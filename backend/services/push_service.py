"""Web Push service — DisasterShield AI

True closed-browser push notifications:
  * generates and persists a VAPID keypair (database/push/vapid_private.pem)
  * stores browser push subscriptions (database/push/subscriptions.json)
  * sends pushes via the Web Push protocol (pywebpush) — Chrome/Edge relay
    through FCM, Firefox through Mozilla's autopush, so alerts arrive in the
    OS notification drawer even when the browser window is closed
  * runs a background daemon inside the Streamlit process that re-checks
    disaster risk every 5 minutes and pushes High/Critical alerts
"""
import json
import time
import logging
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "database" / "push"
KEY_FILE = DATA_DIR / "vapid_private.pem"
SUB_FILE = DATA_DIR / "subscriptions.json"
SENT_FILE = DATA_DIR / "sent_state.json"

VAPID_CLAIMS = {"sub": "mailto:abc@gmail.com"}
CHECK_INTERVAL_S = 300          # risk re-check cadence
RESEND_COOLDOWN_S = 6 * 3600    # don't repeat the same alert for 6 h

_lock = threading.Lock()


# ── VAPID keys ────────────────────────────────────────────────────────────────
def _ensure_keys():
    DATA_DIR.mkdir(exist_ok=True)
    if not KEY_FILE.exists():
        from py_vapid import Vapid
        v = Vapid()
        v.generate_keys()
        v.save_key(str(KEY_FILE))
        logger.info("Generated new VAPID keypair at %s", KEY_FILE)


def get_public_key() -> str:
    """Base64url-encoded uncompressed public key for PushManager.subscribe()."""
    try:
        _ensure_keys()
        from py_vapid import Vapid, b64urlencode
        from cryptography.hazmat.primitives import serialization
        v = Vapid.from_file(str(KEY_FILE))
        raw = v.public_key.public_bytes(
            serialization.Encoding.X962,
            serialization.PublicFormat.UncompressedPoint,
        )
        return b64urlencode(raw)
    except Exception as e:
        logger.error("VAPID public key unavailable: %s", e)
        return ""


# ── Subscription store ────────────────────────────────────────────────────────
def _load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data):
    DATA_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=1), encoding="utf-8")


def save_subscription(sub: dict, lat: float, lon: float) -> bool:
    """Persist a browser push subscription with its monitored location."""
    if not sub or "endpoint" not in sub:
        return False
    with _lock:
        subs = _load_json(SUB_FILE, [])
        subs = [s for s in subs if s["sub"].get("endpoint") != sub["endpoint"]]
        subs.append({"sub": sub, "lat": round(lat, 3), "lon": round(lon, 3),
                     "ts": int(time.time())})
        _save_json(SUB_FILE, subs)
    logger.info("Push subscription saved (%d total)", len(subs))
    return True


def subscription_count() -> int:
    return len(_load_json(SUB_FILE, []))


# ── Sending ───────────────────────────────────────────────────────────────────
def _send(sub: dict, payload: dict) -> bool:
    from pywebpush import webpush, WebPushException
    try:
        webpush(
            subscription_info=sub,
            data=json.dumps(payload),
            vapid_private_key=str(KEY_FILE),
            vapid_claims=dict(VAPID_CLAIMS),
            ttl=3600,
        )
        return True
    except WebPushException as e:
        code = getattr(getattr(e, "response", None), "status_code", None)
        if code in (404, 410):     # subscription expired — prune it
            with _lock:
                subs = _load_json(SUB_FILE, [])
                subs = [s for s in subs
                        if s["sub"].get("endpoint") != sub.get("endpoint")]
                _save_json(SUB_FILE, subs)
            logger.info("Pruned expired push subscription")
        else:
            logger.error("Web push failed: %s", e)
        return False
    except Exception as e:
        logger.error("Web push error: %s", e)
        return False


def send_to_all(title: str, body: str, critical: bool = False, url: str = "/") -> int:
    """Push an alert to every stored subscription. Returns delivered count."""
    _ensure_keys()
    subs = _load_json(SUB_FILE, [])
    sent = 0
    for entry in list(subs):
        if _send(entry["sub"], {"title": title, "body": body,
                                "critical": critical, "url": url,
                                "tag": f"ds-{'crit' if critical else 'warn'}"}):
            sent += 1
    return sent


# ── Background risk-watch daemon ──────────────────────────────────────────────
def _daemon_loop():
    from backend.services.weather_service import get_weather_uncached as get_weather
    from backend.services.risk_engine import predict_risks

    logger.info("Push daemon started (interval %ss)", CHECK_INTERVAL_S)
    while True:
        try:
            subs = _load_json(SUB_FILE, [])
            if subs:
                sent_state = _load_json(SENT_FILE, {})
                now = time.time()
                # one check per unique location, shared by its subscribers
                locations = {(s["lat"], s["lon"]) for s in subs}
                for lat, lon in locations:
                    weather = get_weather(lat, lon)
                    if not weather.get("available"):
                        continue
                    preds = predict_risks(weather)
                    for p in preds:
                        level = p.get("risk_level")
                        if level not in ("High", "Critical"):
                            continue
                        key = f"{lat},{lon}:{p['disaster']}:{level}"
                        if now - sent_state.get(key, 0) < RESEND_COOLDOWN_S:
                            continue
                        critical = level == "Critical"
                        title = (f"🚨 CRITICAL: {p['disaster']}" if critical
                                 else f"⚠️ HIGH RISK: {p['disaster']}")
                        body = p.get("reason",
                                     "Disaster risk detected in your area. "
                                     "Open DisasterShield for guidance.")
                        n = 0
                        for entry in subs:
                            if (entry["lat"], entry["lon"]) == (lat, lon):
                                if _send(entry["sub"],
                                         {"title": title, "body": body,
                                          "critical": critical,
                                          "url": "/emergency",
                                          "tag": f"ds-{p['disaster']}"}):
                                    n += 1
                        if n:
                            sent_state[key] = now
                            logger.info("Pushed '%s' to %d device(s)", title, n)
                _save_json(SENT_FILE, sent_state)
        except Exception as e:
            logger.error("Push daemon iteration failed: %s", e)
        time.sleep(CHECK_INTERVAL_S)


_daemon_started = False


def ensure_daemon():
    """Start the background risk-watch thread once per server process."""
    global _daemon_started
    with _lock:
        if _daemon_started:
            return
        _daemon_started = True
    _ensure_keys()
    t = threading.Thread(target=_daemon_loop, name="ds-push-daemon", daemon=True)
    t.start()

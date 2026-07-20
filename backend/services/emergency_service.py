from backend.services.config import EMERGENCY_CONTACTS


def get_emergency_contacts() -> list[dict]:
    """Return the official Indian emergency contact list."""
    return EMERGENCY_CONTACTS

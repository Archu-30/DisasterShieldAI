/* DisasterShield AI — Push Service Worker
   Receives Web Push messages from the DisasterShield server and shows
   OS notifications even when the browser window is completely closed
   (Chrome keeps a background process for push on desktop; on Android
   pushes arrive via FCM). */

self.addEventListener('install', function (e) {
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(clients.claim());
});

self.addEventListener('push', function (event) {
  var d = {};
  try { d = event.data ? event.data.json() : {}; } catch (err) {}
  var title = d.title || '🛡 DisasterShield Alert';
  var opts = {
    body: d.body || 'A disaster alert has been issued for your area.',
    icon: d.icon || '/app/static/icon.png',
    badge: d.icon || '/app/static/icon.png',
    tag: d.tag || ('ds-push-' + Date.now()),
    renotify: true,
    requireInteraction: !!d.critical,
    vibrate: d.critical ? [200, 100, 200, 100, 400] : [100, 50, 100],
    data: { url: d.url || '/' }
  };
  event.waitUntil(self.registration.showNotification(title, opts));
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (list) {
      for (var i = 0; i < list.length; i++) {
        if ('focus' in list[i]) return list[i].focus();
      }
      return clients.openWindow(event.notification.data.url || '/');
    })
  );
});

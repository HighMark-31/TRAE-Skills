# Skill: PWA Implementation

## Purpose
To convert a web application into a Progressive Web App (PWA) that is installable, works offline, and behaves like a native app.

## When to Use
- When you want a mobile presence without developing separate native apps.
- To improve engagement via "Add to Home Screen".

## Procedure

### 1. Manifest File (`manifest.json`)
Describes the app (name, icons, colors).
```json
{
  "name": "My PWA",
  "short_name": "PWA",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```
Link it in HTML: `<link rel="manifest" href="/manifest.json">`.

### 2. Service Worker (Offline Support)
Intercepts network requests.
1.  **Register**:
    ```javascript
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js');
    }
    ```
2.  **Implement (`sw.js`)**: Use Workbox for easier setup, or raw JS.
    ```javascript
    self.addEventListener('install', (e) => {
      e.waitUntil(caches.open('v1').then((cache) => cache.addAll(['/', '/index.html'])));
    });

    self.addEventListener('fetch', (e) => {
      e.respondWith(caches.match(e.request).then((res) => res || fetch(e.request)));
    });
    ```

### 3. HTTPS
PWAs **require** HTTPS (except on localhost).

### 4. Maskable Icons
Ensure icons have ` "purpose": "any maskable" ` to look good on Android (adaptive icons).

## Constraints
- **iOS Support**: Limited compared to Android (no push notifications until recently, manual install process).
- **Storage**: Browser cache limits apply (usually ~50-100MB guaranteed, more available if requested).

## Expected Output
An installable web app with an "App-like" experience and offline capabilities.

# Skill: Browser Storage

## Purpose
To store data on the client-side efficiently, choosing the right mechanism (LocalStorage, SessionStorage, Cookies, IndexedDB).

## When to Use
- **Cookies**: Auth tokens (HTTPOnly), small preferences.
- **LocalStorage**: Non-sensitive persistent data (Dark mode preference).
- **SessionStorage**: Tab-specific data (Form inputs).
- **IndexedDB**: Large datasets, structured data, files.

## Procedure

### 1. Local/Session Storage (Sync, Key-Value)
Simple API, string only. Limit ~5MB.
```javascript
// Save object
localStorage.setItem('user', JSON.stringify({ name: 'John' }));

// Retrieve
const user = JSON.parse(localStorage.getItem('user'));
```

### 2. IndexedDB (Async, NoSQL-like)
Complex API, supports indexes and transactions. Limit >500MB.
Use a wrapper library like `idb`.
```javascript
import { openDB } from 'idb';

const db = await openDB('my-db', 1, {
  upgrade(db) {
    db.createObjectStore('keyval');
  },
});

await db.put('keyval', 'world', 'hello');
const val = await db.get('keyval', 'hello');
```

### 3. Cookies
Sent with every HTTP request.
```javascript
document.cookie = "username=John; SameSite=Lax; Secure";
```

## Constraints
- **Security**: Never store sensitive data (passwords, credit cards) in LocalStorage/IndexedDB (accessible by XSS).
- **Performance**: LocalStorage is synchronous and blocks the main thread. Avoid large reads/writes.

## Expected Output
Persistent client-side state tailored to data size and security requirements.

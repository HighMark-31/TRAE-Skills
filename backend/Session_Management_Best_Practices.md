# Skill: Session Management Best Practices

## Purpose
To securely manage user sessions, maintaining state across stateless HTTP requests while preventing hijacking and XSS/CSRF attacks.

## When to Use
- Any web application requiring login.
- Choosing between JWT and Server-side Sessions.

## Procedure

### 1. Choice: JWT vs Session Cookies
- **Session Cookies (Stateful)**: Better for security (revocation is easy). ID stored in cookie, data in Redis/DB.
- **JWT (Stateless)**: Better for scalability/microservices. Data signed in token. Harder to revoke.

### 2. Secure Cookie Configuration
Regardless of the method, store the token/ID in a **HttpOnly** cookie.
```javascript
res.cookie('session_id', token, {
  httpOnly: true, // Prevents JS access (XSS protection)
  secure: process.env.NODE_ENV === 'production', // HTTPS only
  sameSite: 'strict', // CSRF protection
  maxAge: 24 * 60 * 60 * 1000 // 1 day
});
```

### 3. Session Store (for Stateful)
Don't use memory store in production. Use Redis.
```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true, httpOnly: true }
}));
```

### 4. Rotation & Expiry
- **Regenerate Session ID** on login to prevent Session Fixation attacks.
    ```javascript
    req.session.regenerate((err) => {
      // save new session
    });
    ```
- Implement **absolute timeouts** (e.g., force re-login after 7 days) and **idle timeouts** (logout after 30m inactivity).

## Constraints
- **Mobile Apps**: Often prefer JWT in Authorization header (`Bearer token`) rather than cookies, as they don't have a browser environment.
- **Size**: Cookies have a 4KB limit. Don't store large data in them.

## Expected Output
A secure authentication state mechanism resilient to common web attacks.

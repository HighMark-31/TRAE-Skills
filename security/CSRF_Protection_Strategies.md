# Skill: CSRF Protection Strategies

## Purpose
To prevent cross-site request forgery.

## When to Use
- Tokens and SameSite cookies.
- When the specific requirement for CSRF Protection Strategies arises in the project.

## Procedure

### 1. SameSite Cookie Attribute
The simplest defense. Set the `SameSite` attribute on your session cookies.
- **Lax**: (Default in modern browsers) Cookies are sent on top-level navigations but blocked on cross-site subrequests (like POST).
- **Strict**: Cookies are only sent if the request originates from the same site.

```javascript
res.cookie('session_id', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'Lax' // Recommended for most apps
});
```

### 2. Synchronizer Token Pattern (CSRF Tokens)
For older browsers or APIs that don't rely solely on cookies.
1. Backend generates a unique, unguessable token per session.
2. Token is sent to the client (e.g., in a hidden form field or a custom header).
3. Client includes this token in every state-changing request (POST, PUT, DELETE).
4. Backend validates the token before processing the request.

```javascript
// Express with 'csurf' (Note: check for updated alternatives as csurf is deprecated)
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.post('/process', csrfProtection, (req, res) => {
  res.send('data processed');
});
```

### 3. Double Submit Cookie Pattern
Used in stateless SPAs.
1. Generate a random value and store it in a cookie (non-httpOnly) and also as a custom header in the request.
2. The backend verifies that the cookie value and the header value match.

### 4. Custom Request Headers
Since scripts cannot set custom headers on cross-origin requests (unless CORS is explicitly configured), checking for a custom header like `X-Requested-With` or a specific API header can provide protection.

## Constraints
- **GET Requests**: NEVER perform state-changing operations in a GET request; CSRF protection usually only applies to POST/PUT/DELETE.
- **CORS**: Misconfigured CORS (e.g., `Access-Control-Allow-Origin: *`) can bypass CSRF protections.
- **Mobile Apps**: CSRF is primarily a browser-based vulnerability; native mobile apps are generally not affected unless they use WebViews.

## Expected Output
An application where cross-origin malicious sites cannot perform actions on behalf of an authenticated user.

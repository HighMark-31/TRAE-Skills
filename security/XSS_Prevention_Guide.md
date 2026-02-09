# Skill: XSS Prevention Guide

## Purpose
To prevent cross-site scripting.

## When to Use
- Sanitization and escaping.
- When the specific requirement for XSS Prevention Guide arises in the project.

## Procedure

### 1. Data Escaping (Output)
Always escape data before rendering it in HTML, attributes, or JavaScript.

```javascript
// Example: Escaping for HTML body
function escapeHTML(str) {
  const p = document.createElement('p');
  p.textContent = str;
  return p.innerHTML;
}

// In React/Vue, this is handled automatically unless using dangerouslySetInnerHTML
const UserComment = ({ text }) => <div>{text}</div>; 
```

### 2. Data Sanitization (Input)
Sanitize HTML input if you must allow some tags (e.g., in a CMS).

```javascript
import sanitizeHtml from 'sanitize-html';

const dirty = '<script>alert("xss")</script><b>Hello</b>';
const clean = sanitizeHtml(dirty, {
  allowedTags: ['b', 'i', 'em', 'strong', 'a'],
  allowedAttributes: {
    'a': ['href']
  }
});
// Result: <b>Hello</b>
```

### 3. Content Security Policy (CSP)
Implement a strict CSP header to block unauthorized scripts.

```javascript
// Express with Helmet.js
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "trusted-scripts.com"],
    objectSrc: ["'none'"],
    upgradeInsecureRequests: [],
  },
}));
```

### 4. HTTP-Only Cookies
Store sensitive data (like JWTs) in `HttpOnly` cookies to prevent access via `document.cookie`.

```javascript
res.cookie('token', jwt, {
  httpOnly: true,
  secure: true, // Only over HTTPS
  sameSite: 'Strict'
});
```

## Constraints
- **Context Awareness**: Escaping for an HTML attribute (e.g., `href`) is different from escaping for an HTML body.
- **Avoid InnerHTML**: Use `textContent` or `innerText` instead of `innerHTML` whenever possible.
- **No Inline Scripts**: Avoid `onclick`, `onmouseover`, etc., and inline `<script>` tags.

## Expected Output
An application that effectively neutralizes malicious scripts injected by users, protecting other users from session hijacking and data theft.

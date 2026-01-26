# Skill: JWT Authentication Implementation

## Purpose
To secure API endpoints by issuing and verifying JSON Web Tokens (JWT) for stateless user authentication.

## When to Use
- When implementing login/signup functionality.
- When protecting private API routes.
- When building Single Page Applications (SPAs) or mobile app backends.

## Procedure
1.  **Install Dependencies**: `jsonwebtoken`, `bcrypt` (for password hashing).
2.  **Login Endpoint**:
    - Verify email/password.
    - If valid, sign a JWT using a secret key (`process.env.JWT_SECRET`).
    - Include `userId` and `role` in the payload. Set an expiration time.
    - Return token to client.
3.  **Auth Middleware**:
    - Extract token from `Authorization: Bearer <token>` header.
    - Verify token using `jwt.verify()`.
    - If valid, attach decoded user data to `req.user`.
    - If invalid/expired, return 401 Unauthorized.
4.  **Protect Routes**: Apply the auth middleware to protected routes.

## Constraints
- Use HTTPS to prevent token interception.
- Do not store sensitive data (passwords) in the JWT payload.
- Use strong, long random strings for `JWT_SECRET`.
- Consider using short-lived access tokens and refresh tokens for better security.

## Expected Output
A secure authentication flow including a token generation utility, a login controller, and an authentication middleware.

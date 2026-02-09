# Skill: JWT Authentication Implementation

## Purpose
To secure API endpoints by issuing and verifying JSON Web Tokens (JWT) for stateless user authentication in Node.js applications.

## When to Use
- When implementing login/signup for SPAs or mobile apps.
- When you need a stateless way to manage user sessions.
- When building microservices that need to share user identity.

## Procedure

### 1. Token Generation Utility
Create a utility to sign tokens with specific expiration times.

```typescript
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET!;
const ACCESS_TOKEN_EXPIRY = '15m';
const REFRESH_TOKEN_EXPIRY = '7d';

export const generateTokens = (userId: string, role: string) => {
  const accessToken = jwt.sign(
    { sub: userId, role },
    JWT_SECRET,
    { expiresIn: ACCESS_TOKEN_EXPIRY }
  );

  const refreshToken = jwt.sign(
    { sub: userId },
    process.env.REFRESH_SECRET!,
    { expiresIn: REFRESH_TOKEN_EXPIRY }
  );

  return { accessToken, refreshToken };
};
```

### 2. Authentication Middleware
Verify the token in the `Authorization` header.

```typescript
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

export const authenticateJWT = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;

  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.split(' ')[1];

    jwt.verify(token, process.env.JWT_SECRET!, (err, decoded) => {
      if (err) {
        return res.sendStatus(403); // Forbidden
      }
      req.user = decoded; // Attach user info to request
      next();
    });
  } else {
    res.sendStatus(401); // Unauthorized
  }
};
```

### 3. Password Hashing (Bcrypt)
Secure passwords before storing them in the database.

```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

export const hashPassword = async (password: string) => {
  return await bcrypt.hash(password, SALT_ROUNDS);
};

export const comparePassword = async (password: string, hash: string) => {
  return await bcrypt.compare(password, hash);
};
```

### 4. Refresh Token Pattern
Handle token rotation for long-lived sessions.

```typescript
// POST /refresh-token
// 1. Verify refresh token from cookie/body
// 2. Check if refresh token is in database (to allow revoking)
// 3. Generate new access token
```

## Constraints
- **Payload Size**: Keep the JWT payload small (only ID, roles, and necessary flags).
- **Secrets**: Never commit `JWT_SECRET` to version control. Use a long, random string.
- **Expiration**: Use short-lived access tokens (15m-1h) and longer-lived refresh tokens.
- **Algorithms**: Use `HS256` (symmetric) or `RS256` (asymmetric/public-private keys).

## Expected Output
A robust authentication system that securely handles password storage, token issuance, and route protection.

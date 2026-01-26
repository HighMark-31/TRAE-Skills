# Authentication Strategy Selection

## Strategies
1. **Session-Based**: Server stores session ID in cookie/DB. Simple, stateful. Good for monoliths.
2. **JWT (Stateless)**: Server signs token, client stores it. Good for microservices/mobile. Harder to revoke.
3. **OAuth/OIDC**: Delegated auth (Login with Google). Best for user convenience and security.
4. **Passwordless**: Magic links, OTPs. Reduces friction.

## Security Considerations
- Always use HTTPS.
- Store passwords using bcrypt/argon2.
- Use `httpOnly` and `secure` cookies for storage where possible to prevent XSS.

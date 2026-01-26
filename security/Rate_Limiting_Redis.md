# Skill: Rate Limiting (Redis)

## Purpose
To protect the API from abuse, brute-force attacks, and denial-of-service (DoS) attempts by limiting the number of requests a client can make within a specific time window.

## When to Use
- When exposing public APIs.
- When protecting sensitive endpoints like login or password reset.
- When preventing resource exhaustion.

## Procedure
1.  **Choose Strategy**:
    - Fixed Window Counter (simple).
    - Sliding Window Log (more accurate).
    - Token Bucket.
2.  **Setup Storage**: Use Redis for distributed state (fast, shared across instances).
3.  **Implement/Configure Middleware**:
    - Use a library like `rate-limiter-flexible` or `express-rate-limit` with Redis store.
    - Define `key` (IP address or User ID).
    - Define `points` (max requests) and `duration` (time window in seconds).
4.  **Handle Rejection**:
    - If limit exceeded, return 429 Too Many Requests.
    - Include `Retry-After` header.
5.  **Apply**:
    - Global limiter for general traffic.
    - Stricter limiter for sensitive routes (e.g., `/login`).

## Constraints
- Ensure Redis failure does not block legitimate traffic (fail open or fallback to memory).
- Whitelist trusted IPs (e.g., internal services, load balancers) if necessary.
- Be careful with IP-based limiting behind proxies (use `X-Forwarded-For`).

## Expected Output
A configured rate limiting middleware integrated into the Express application, backed by Redis.

# Skill: Rate Limiting (Redis)

## Purpose
To protect APIs from abuse, brute-force attacks, and DoS attempts by limiting the number of requests a client can make within a specific time window.

## When to Use
- When exposing public APIs to the internet.
- When protecting high-cost endpoints (e.g., AI generation, email sending).
- When securing login and password reset routes.

## Procedure

### 1. Installation
Use `rate-limiter-flexible` for a robust, Redis-backed implementation.

```bash
npm install rate-limiter-flexible redis
```

### 2. Redis Client Setup
Initialize the Redis client for the limiter.

```typescript
import { createClient } from 'redis';

const redisClient = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

redisClient.connect().catch(console.error);
```

### 3. Implementing the Limiter
Create a reusable limiter instance.

```typescript
import { RateLimiterRedis } from 'rate-limiter-flexible';

const loginLimiter = new RateLimiterRedis({
  storeClient: redisClient,
  keyPrefix: 'login_fail_limit',
  points: 5, // 5 requests
  duration: 60 * 15, // per 15 minutes
  blockDuration: 60 * 60, // Block for 1 hour if limit exceeded
});
```

### 4. Express Middleware Implementation
Apply the limiter to specific routes.

```typescript
import { Request, Response, NextFunction } from 'express';

export const rateLimitMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const key = req.ip; // Use IP address as key
    await loginLimiter.consume(key);
    next();
  } catch (rejRes) {
    res.status(429).json({
      error: 'Too Many Requests',
      retryAfter: Math.round(rejRes.msBeforeNext / 1000) || 1
    });
  }
};
```

### 5. Advanced: Dynamic Limits
Adjust limits based on user role or API key tier.

```typescript
const getLimitByTier = (user) => {
  if (user.isPremium) return 100;
  return 10;
};
```

## Constraints
- **Fail-Open vs Fail-Closed**: Decide if the API should stay open if Redis is down. Usually, fail-open is safer for UX.
- **Trust Proxy**: If behind a load balancer (Nginx, Cloudflare), set `app.set('trust proxy', 1)` in Express to get the correct client IP.
- **Key Selection**: Use IP for anonymous users, UserID for authenticated users to prevent bypass via IP rotation.

## Expected Output
A production-ready rate-limiting layer that prevents abuse while providing clear feedback to users when limits are hit.

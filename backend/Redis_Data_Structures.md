# Skill: Redis Data Structures

## Purpose
To utilize Redis beyond simple key-value caching by leveraging its advanced data structures for high-performance use cases like leaderboards, queues, and real-time analytics.

## When to Use
- **Lists/Streams**: For message queues or activity feeds.
- **Sets**: For unique collections (e.g., tags, online users).
- **Sorted Sets**: For leaderboards or priority queues.
- **Hashes**: For storing object-like data (e.g., user profiles) efficiently.
- **HyperLogLog**: For probabilistic counting (e.g., unique visitors) with minimal memory.

## Procedure

### 1. Connection
Using `ioredis` (Node.js):
```javascript
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);
```

### 2. Common Patterns

#### A. Leaderboards (Sorted Sets)
Use `ZADD` to add scores and `ZREVRANGE` to get top users.
```javascript
// Add user score
await redis.zadd('leaderboard', 100, 'user:1');
await redis.zadd('leaderboard', 150, 'user:2');

// Get top 10
const topUsers = await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');
```

#### B. Caching Objects (Hashes)
Use `HSET` and `HGETALL`.
```javascript
// Store user profile
await redis.hset('user:100', {
  name: 'John',
  email: 'john@example.com',
  login_count: 5
});

// Retrieve
const user = await redis.hgetall('user:100');
```

#### C. Rate Limiting (Strings with Expiry)
Simple atomic counter pattern.
```javascript
const key = `rate_limit:${ip}`;
const current = await redis.incr(key);
if (current === 1) {
  await redis.expire(key, 60); // 1 minute window
}
if (current > 100) throw new Error("Rate limit exceeded");
```

## Constraints
- **Memory**: Redis stores everything in RAM. Use `maxmemory` policy (e.g., `allkeys-lru`) to evict old data if cache fills up.
- **Persistence**: Configure RDB or AOF if data durability is required (not just caching).

## Expected Output
Efficient data storage and retrieval patterns tailored to specific application needs, reducing load on the primary database.

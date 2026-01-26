# Skill: Caching Strategy (Redis)

## Purpose
To improve response times and reduce database load by storing frequently accessed data in a fast, in-memory store.

## When to Use
- When fetching data that changes infrequently (e.g., product catalog, configuration).
- When computing expensive aggregations.
- When endpoints have high read-to-write ratios.

## Procedure
1.  **Identify Data**: Determine what to cache and for how long (TTL).
2.  **Check Cache First**:
    - Construct a unique cache key (e.g., `product:123`).
    - Query Redis for the key.
    - If found (Hit), return JSON parsed data immediately.
3.  **Fetch on Miss**:
    - If not found (Miss), query the primary database.
    - Save the result to Redis with an expiration (`SETEX key ttl value`).
    - Return the data.
4.  **Invalidation Strategy**:
    - Determine how to handle updates (Cache-Aside is common).
    - When data is updated/deleted, delete the corresponding Redis key.

## Constraints
- Handle cache stampedes (many requests for same missing key at once).
- Ensure data consistency (don't serve stale data longer than acceptable).
- Serialize/deserialize objects correctly (Redis stores strings/buffers).

## Expected Output
A caching utility or middleware that transparently handles cache hits and misses, significantly reducing API latency.

# Skill: PostgreSQL Indexing

## Purpose
To optimize database query performance by applying appropriate indexing strategies in PostgreSQL.

## When to Use
- When queries are slow (high execution time).
- When filtering, sorting, or joining on specific columns frequently.
- To enforce uniqueness constraints.

## Procedure

### 1. Analyze Queries
Use `EXPLAIN ANALYZE` to check if an index is being used.
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@test.com';
-- Look for "Index Scan" vs "Seq Scan" (Sequential Scan)
```

### 2. Index Types

#### A. B-Tree (Default)
Good for equality (`=`) and range (`<`, `>`, `BETWEEN`) queries.
```sql
CREATE INDEX idx_users_email ON users(email);
```

#### B. Hash
Good only for equality checks (`=`), smaller than B-Tree but crash-safe only in recent versions. Generally B-Tree is preferred.

#### C. GIN (Generalized Inverted Index)
Essential for JSONB and Full-Text Search.
```sql
-- For JSONB
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);
-- Query: WHERE metadata @> '{"role": "admin"}'
```

#### D. Partial Indexes
Index only a subset of rows to save space.
```sql
CREATE INDEX idx_active_orders ON orders(created_at) WHERE status = 'active';
```

### 3. Maintenance
Indexes slow down write operations (INSERT/UPDATE).
- Remove unused indexes.
- Periodically `REINDEX` if bloat occurs (though autovacuum handles most cleanup).

## Constraints
- **Write Performance**: Adding too many indexes degrades write speed.
- **Selectivity**: Indexes are useless for low-cardinality columns (e.g., `gender` with only 2 values) unless using partial indexes.

## Expected Output
Significant reduction in query execution time (from seconds to milliseconds) for targeted read operations.

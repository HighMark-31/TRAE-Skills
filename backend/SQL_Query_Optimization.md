# Skill: SQL Query Optimization

## Purpose
To improve database performance by writing efficient SQL queries, using indexes correctly, and avoiding common pitfalls like N+1 problems.

## When to Use
- When an API endpoint is slow due to database latency.
- When reviewing database access patterns in code reviews.
- When dealing with large datasets.

## Procedure
1.  **Analyze Query Plan**: Use `EXPLAIN ANALYZE` (Postgres) or equivalent to understand execution path. Look for "Seq Scan" on large tables.
2.  **Add Indexes**:
    - Index columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses.
    - Use composite indexes for multi-column queries (order matters: equality first, then range).
3.  **Optimize Selects**:
    - Select only necessary columns (`SELECT id, name` vs `SELECT *`).
    - Avoid `SELECT *` in production code.
4.  **Fix N+1 Problems**:
    - Use eager loading (`JOIN` or `.withGraphFetched()` in ORMs) instead of iterating and querying in a loop.
5.  **Refactor Complex Logic**:
    - Move complex data manipulation to the database (aggregations, window functions) if it reduces data transfer.
    - Batch inserts/updates instead of one-by-one.

## Constraints
- Do not over-index (indexes slow down writes).
- Avoid functions on indexed columns in `WHERE` clauses (prevents index usage).
- Test performance with realistic data volumes.

## Expected Output
Optimized SQL queries or ORM calls that execute significantly faster and consume fewer resources.

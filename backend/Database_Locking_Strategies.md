# Skill: Database Locking Strategies

## Purpose
To manage concurrent access to database records, preventing race conditions and data inconsistencies (e.g., double spending, overbooking).

## When to Use
- Financial transactions.
- Inventory management.
- "Check-and-Set" operations.

## Procedure

### 1. Optimistic Locking (Versioning)
Assume conflict is rare. Use a `version` column.
1.  Read record: `SELECT * FROM products WHERE id=1;` (Returns version: 5)
2.  Update with check:
    ```sql
    UPDATE products SET stock = stock - 1, version = 6
    WHERE id = 1 AND version = 5;
    ```
3.  Check result: If "0 rows affected", someone else modified it. Retry or throw error.

**Implementation (TypeORM/Prisma)**:
Often supported natively (`@VersionColumn` in TypeORM).

### 2. Pessimistic Locking
Assume conflict is likely. Lock the row for the transaction duration.
1.  Start Transaction.
2.  Select for Update:
    ```sql
    SELECT * FROM products WHERE id = 1 FOR UPDATE;
    ```
    (This blocks other transactions trying to lock this row).
3.  Perform Logic.
4.  Commit (Release Lock).

### 3. Advisory Locks (App Level)
Lock an arbitrary abstract name/ID, not a specific row.
```sql
-- PostgreSQL
SELECT pg_advisory_xact_lock(12345);
-- Do work...
-- Lock released automatically at end of transaction
```

## Constraints
- **Deadlocks**: Pessimistic locking can lead to deadlocks if two transactions lock resources in reverse order. Always acquire locks in a consistent order (e.g., sort by ID).
- **Performance**: `FOR UPDATE` reduces concurrency. Use Optimistic locking for high-traffic, low-conflict scenarios.

## Expected Output
Data integrity guarantees under high concurrency, ensuring atomic transitions of state.

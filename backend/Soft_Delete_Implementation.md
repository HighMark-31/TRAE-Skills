# Skill: Soft Delete Implementation

## Purpose
To mark records as deleted without physically removing them from the database, allowing for data recovery and audit trails.

## When to Use
- When data is valuable or legally required to be retained.
- When "deleting" a user account or order.

## Procedure
1.  **Schema Change**: Add a `deletedAt` (timestamp) column to the table. Nullable.
2.  **Modify Delete Logic**:
    - Instead of `DELETE FROM table`, perform `UPDATE table SET deletedAt = NOW()`.
3.  **Modify Read Logic**:
    - Filter queries globally or per-query: `WHERE deletedAt IS NULL`.
4.  **Cascade**: Decide how to handle related records (soft delete them too, or just hide them via the parent's status).
5.  **Restore**: Implement a `restore` method that sets `deletedAt = NULL`.

## Constraints
- Unique indexes might conflict (e.g., email must be unique, but a soft-deleted user has the email). Solution: Include `deletedAt` in the unique index or use partial indexes.
- Remember to filter soft-deleted records in *every* select query.

## Expected Output
A data access layer that transparently handles soft deletion and filtering, ensuring deleted items don't appear in normal results.

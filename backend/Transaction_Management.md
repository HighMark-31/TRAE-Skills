# Skill: Transaction Management

## Purpose
To ensure data integrity by grouping multiple database operations into a single atomic unit. Either all operations succeed, or none do.

## When to Use
- Transferring money (debit A, credit B).
- Creating an order (create order, create items, update inventory).
- Any multi-step write operation.

## Procedure
1.  **Start Transaction**: Begin the transaction via the ORM/DB client.
2.  **Execute Operations**: Run the sequence of DB commands, passing the transaction object/context to each.
3.  **Commit**: If all steps succeed, commit the transaction to persist changes.
4.  **Rollback**: If any step throws an error, catch it and rollback the transaction to revert all changes.
5.  **Release**: Release the connection back to the pool.

## Constraints
- Keep transactions short to avoid locking tables for too long.
- Do not perform external API calls inside a transaction (if the API succeeds but DB fails, you can't rollback the API).

## Expected Output
A robust function wrapper or pattern that handles the begin/commit/rollback lifecycle for complex operations.

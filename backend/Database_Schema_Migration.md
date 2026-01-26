# Skill: Database Schema Migration

## Purpose
To safely modify the database schema (tables, columns, indexes) using version-controlled migration files, ensuring consistency across development, staging, and production environments.

## When to Use
- When adding new tables or columns.
- When modifying column types or constraints.
- When adding indexes for performance.
- When seeding initial reference data.

## Procedure
1.  **Generate Migration File**: Use the ORM/Query Builder CLI (e.g., Knex, TypeORM, Prisma) to create a new migration file with a timestamp prefix.
2.  **Implement `up` Method**:
    - Define the changes to apply (e.g., `createTable`, `alterTable`).
    - Ensure correct data types and constraints (NOT NULL, DEFAULT).
    - Add foreign keys with appropriate `onDelete` behavior (CASCADE, SET NULL).
3.  **Implement `down` Method**:
    - Define the exact reverse of the `up` method.
    - Ensure data loss warnings are considered if dropping tables/columns.
4.  **Review SQL**: If possible, inspect the generated SQL to ensure it performs efficiently (e.g., avoiding table locks on large tables if possible).
5.  **Test Migration**: Run `migrate:up` and `migrate:down` locally to verify reversibility.

## Constraints
- Never modify an existing migration file that has already been committed/deployed. Create a new one.
- Avoid logic that depends on application code within migrations (migrations should be standalone SQL/schema logic).
- Ensure migrations are idempotent where possible.

## Expected Output
A valid migration file in the project's migrations directory that successfully alters the database schema when run and reverts cleanly when rolled back.

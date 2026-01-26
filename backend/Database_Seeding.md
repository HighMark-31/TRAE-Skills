# Skill: Database Seeding

## Purpose
To populate the database with predictable, realistic initial data for development, testing, and staging environments.

## When to Use
- When setting up a new developer machine.
- When running integration tests (resetting state).
- When initializing a new environment with lookup data (e.g., roles, categories).

## Procedure
1.  **Select Library**: Use a faker library (e.g., `@faker-js/faker`) to generate random realistic data.
2.  **Define Factories**: Create functions that generate a single valid object for each entity (e.g., `makeUser()`).
3.  **Define Seeder Script**:
    - Connect to DB.
    - Clear existing data (optional/careful).
    - Loop and insert data using factories.
    - Maintain referential integrity (create Users first, then Posts).
4.  **Idempotency**: Check if data exists before inserting (if running on persistent envs).
5.  **Run Command**: Add `npm run seed` script.

## Constraints
- NEVER run destructive seeds against production databases (add safety checks).
- Ensure seeded data passes all validation rules.
- Keep seed execution time reasonable.

## Expected Output
A seed script that, when executed, populates the database with a rich set of test data.

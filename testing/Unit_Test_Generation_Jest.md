# Skill: Unit Test Generation (Jest)

## Purpose
To create robust unit tests for individual functions, classes, or modules to ensure they behave as expected in isolation.

## When to Use
- When writing new business logic or utility functions.
- When fixing a bug (write a failing test first).
- When refactoring code to ensure no regressions.

## Procedure
1.  **Identify Unit**: Select the function or class to test.
2.  **Mock Dependencies**: Identify external dependencies (DB, APIs, other modules) and mock them using `jest.mock()` or dependency injection.
3.  **Write Test Cases**:
    - **Happy Path**: Test with valid inputs and verify expected output.
    - **Edge Cases**: Test with empty, null, undefined, or boundary values.
    - **Error Handling**: Test that the function throws or handles errors correctly when dependencies fail or inputs are invalid.
4.  **Assert Outcomes**: Use `expect()` to verify return values, function calls (`toHaveBeenCalled`), and state changes.
5.  **Run and Refine**: Run the test suite and ensure it passes. Improve coverage if needed.

## Constraints
- Unit tests must NOT access the real database or network. Use mocks/stubs.
- Tests should be independent and order-agnostic.
- Aim for high branch coverage, not just line coverage.

## Expected Output
A `*.test.ts` or `*.spec.ts` file containing a `describe` block with multiple `it` or `test` cases covering the logic of the target unit.

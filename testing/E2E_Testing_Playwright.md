# Skill: E2E Testing (Cypress/Playwright)

## Purpose
To simulate real user scenarios from start to finish, ensuring that the integrated system (Frontend + Backend + Database) works as expected.

## When to Use
- Testing critical flows: Login, Checkout, Registration.
- Ensuring no regressions in core business logic.

## Procedure
1.  **Install Tool**: `npm init playwright@latest` or `npm install cypress`.
2.  **Define Spec**: Create a test file (e.g., `login.spec.ts`).
3.  **Write Test**:
    - Visit the page: `await page.goto('/login')`.
    - Interact: `await page.fill('input[name="email"]', 'user@example.com')`.
    - Click: `await page.click('button[type="submit"]')`.
    - Assert: `await expect(page).toHaveURL('/dashboard')`.
4.  **Mocking (Optional)**: Intercept network requests if you want to test frontend in isolation, but true E2E hits the real backend.
5.  **Run**: Execute in CI pipeline (headless mode).

## Constraints
- E2E tests are slow and flaky; use them for critical paths only.
- Ensure the test environment is clean (seed data before test).
- Use stable selectors (`data-testid`) instead of fragile CSS classes.

## Expected Output
A suite of automated browser tests that verify user journeys function correctly.

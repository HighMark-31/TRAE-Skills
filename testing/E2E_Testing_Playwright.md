# Skill: E2E Testing (Cypress/Playwright)

## Purpose
To simulate real user scenarios from start to finish, ensuring that the integrated system (Frontend + Backend + Database) works as expected.

## When to Use
- Testing critical flows: Login, Checkout, Registration.
- Ensuring no regressions in core business logic.

## Procedure

### 1. Installation
Initialize Playwright in your project.

```bash
npm init playwright@latest
# Choose TypeScript, add GitHub Actions workflow, etc.
```

### 2. Writing a Test Case
Create a spec file in the `tests/` directory.

```typescript
import { test, expect } from '@playwright/test';

test('user can login and see dashboard', async ({ page }) => {
  // 1. Arrange
  await page.goto('/login');

  // 2. Act
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Log in' }).click();

  // 3. Assert
  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible();
});
```

### 3. Page Object Model (POM)
Organize code into reusable Page Objects for better maintainability.

```typescript
// models/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}
  async goto() { await this.page.goto('/login'); }
  async login(email, pass) {
    await this.page.fill('#email', email);
    await this.page.fill('#pass', pass);
    await this.page.click('#submit');
  }
}
```

### 4. Running Tests
Execute tests in different modes.

```bash
# Run all tests (headless)
npx playwright test

# Run with UI (best for debugging)
npx playwright test --ui

# Run specific file
npx playwright test login.spec.ts
```

## Constraints
- **Test Independence**: Each test should be able to run in isolation. Use `test.beforeEach` to reset state.
- **Avoid Fragile Selectors**: Use `getByRole`, `getByLabel`, or `data-testid` instead of classes like `.btn-primary`.
- **Wait Strategically**: Use Playwright's auto-waiting features; avoid `page.waitForTimeout(3000)`.

## Expected Output
A set of robust E2E tests that reliably verify critical user journeys across different browsers.

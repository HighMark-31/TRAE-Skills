# Skill: Unit Test Generation (Jest)

## Purpose
To create robust unit tests for individual functions, classes, or modules to ensure they behave as expected in isolation.

## When to Use
- When writing new business logic or utility functions.
- When fixing a bug (write a failing test first).
- When refactoring code to ensure no regressions.

## Procedure

### 1. Setup Jest
Ensure Jest is configured for your project (e.g., in `package.json` or `jest.config.js`).

```bash
npm install --save-dev jest ts-jest @types/jest
```

### 2. Implementation: Basic Unit Test
Test a pure function.

```typescript
// math.ts
export const add = (a: number, b: number) => a + b;

// math.test.ts
import { add } from './math';

describe('add function', () => {
  it('should correctly add two positive numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
});
```

### 3. Implementation: Mocking Dependencies
Use `jest.mock()` to isolate the unit under test.

```typescript
// userService.test.ts
import { getUser } from './userService';
import { db } from './db';

jest.mock('./db'); // Mock the database module

describe('getUser', () => {
  it('should return a user if found in DB', async () => {
    (db.findUser as jest.Mock).mockResolvedValue({ id: 1, name: 'Alice' });
    
    const user = await getUser(1);
    expect(user.name).toBe('Alice');
    expect(db.findUser).toHaveBeenCalledWith(1);
  });
});
```

### 4. Testing Asynchronous Code
Use `async/await` in your test cases.

```typescript
it('should throw error if API fails', async () => {
  api.getData.mockRejectedValue(new Error('Network error'));
  await expect(fetchData()).rejects.toThrow('Network error');
});
```

### 5. Running with Coverage
Verify how much of your code is tested.

```bash
npm test -- --coverage
```

## Constraints
- **Isolate**: Never call real databases, file systems, or external APIs.
- **Speed**: Unit tests should be extremely fast (hundreds per second).
- **Descriptive Names**: Use clear `describe` and `it` blocks (e.g., `it('should return 400 when email is invalid')`).

## Expected Output
A high-coverage test suite that gives developers confidence when refactoring or adding new features.

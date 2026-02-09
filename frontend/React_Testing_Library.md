# Skill: React Testing Library (RTL)

## Purpose
To test React components by interacting with them as a user would (clicking, typing, reading text), rather than testing implementation details.

## When to Use
- Unit and Integration testing of UI components.
- Ensuring accessibility (finding elements by role).

## Procedure

### 1. Philosophy
"The more your tests resemble the way your software is used, the more confidence they can give you."
- **Do**: `screen.getByRole('button', { name: /submit/i })`
- **Don't**: `container.querySelector('.btn-primary')`

### 2. Basic Test
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Counter from './Counter';

test('increments counter', () => {
  render(<Counter />);
  
  // Assert initial state
  expect(screen.getByText('Count: 0')).toBeInTheDocument();
  
  // Act
  fireEvent.click(screen.getByRole('button', { name: /increment/i }));
  
  // Assert new state
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

### 3. User Event (Recommended)
`user-event` simulates real browser interactions better than `fireEvent`.
```tsx
import userEvent from '@testing-library/user-event';

test('typing', async () => {
  const user = userEvent.setup();
  render(<Input />);
  await user.type(screen.getByRole('textbox'), 'Hello');
});
```

## Constraints
- **Async**: Use `findBy...` (returns Promise) for elements that appear after an API call/timeout.
- **Mocking**: Mock external modules (API calls) using Jest/Vitest `vi.mock` to keep tests fast and isolated.

## Expected Output
Robust test suite ensuring components behave correctly from the user's perspective.

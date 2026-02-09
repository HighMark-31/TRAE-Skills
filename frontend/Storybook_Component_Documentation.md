# Skill: Storybook Component Documentation

## Purpose
To develop, test, and document UI components in isolation from the main application.

## When to Use
- Building a Design System.
- Visual testing.
- Collaborating with designers.

## Procedure

### 1. Setup
```bash
npx storybook@latest init
```

### 2. Writing Stories
A story captures a specific state of a component.
`Button.stories.tsx`:
```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  component: Button,
  title: 'Components/Button',
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    primary: true,
    label: 'Button',
  },
};

export const Secondary: Story = {
  args: {
    label: 'Button',
  },
};
```

### 3. Addons
- **Controls**: Edit props dynamically in the UI.
- **Actions**: Log events (clicks).
- **Docs**: Auto-generate documentation from comments (JSDoc).

### 4. Testing
Use Interaction Testing (play function) to simulate user behavior within Storybook.

## Constraints
- **Maintenance**: Stories must be updated when component props change.
- **Context**: Components relying on global providers (Redux, Router) need decorators in `.storybook/preview.js` to work.

## Expected Output
A living style guide where every component state is cataloged and interactive.

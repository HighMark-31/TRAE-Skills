# Skill: Custom React Hook Creation

## Purpose
To extract reusable logic from components, making code cleaner, more modular, and easier to test.

## When to Use
- When logic is duplicated across multiple components.
- When a component is too large and complex.
- Examples: `useFetch`, `useLocalStorage`, `useWindowSize`, `useAuth`.

## Procedure
1.  **Name Hook**: Start with `use` (e.g., `useToggle`).
2.  **Define Logic**:
    - Declare state (`useState`, `useReducer`).
    - Declare side effects (`useEffect`).
3.  **Return Interface**: Return an array or object containing the state and functions to manipulate it.
    - Example: `return [value, toggleValue]`.
4.  **Usage**: Import and call it in a component: `const [isOn, toggle] = useToggle(false)`.

## Constraints
- Hooks must only be called at the top level of a component (Rules of Hooks).
- Do not put JSX in a custom hook (usually). It should return data/logic, not UI.

## Expected Output
A standalone TypeScript/JavaScript file exporting a function that encapsulates specific stateful logic.

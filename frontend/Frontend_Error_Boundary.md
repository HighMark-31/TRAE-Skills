# Skill: Frontend Error Boundary

## Purpose
To catch JavaScript errors anywhere in the child component tree, log those errors, and display a fallback UI instead of the component tree crashing and showing a blank screen.

## When to Use
- Wrapping the entire application (Global Error Boundary).
- Wrapping major widgets (so one widget crashing doesn't break the whole page).

## Procedure
1.  **Create Class Component**: Error Boundaries *must* be class components (until React adds a hook).
    - `class ErrorBoundary extends React.Component { ... }`.
2.  **Implement State**: `state = { hasError: false }`.
3.  **Implement Lifecycle**:
    - `static getDerivedStateFromError(error)`: Update state to show fallback.
    - `componentDidCatch(error, info)`: Log error to reporting service (Sentry).
4.  **Render**:
    - If `hasError`, return `<h1>Something went wrong.</h1>`.
    - Else, return `this.props.children`.
5.  **Usage**: Wrap components: `<ErrorBoundary><MyWidget /></ErrorBoundary>`.

## Constraints
- Error Boundaries do *not* catch errors in: Event handlers, Asynchronous code (setTimeout), Server-side rendering.
- Use a library like `react-error-boundary` for a more modern/hook-friendly approach.

## Expected Output
A resilient application that degrades gracefully when unexpected runtime errors occur.

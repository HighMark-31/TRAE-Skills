# Skill: React Component Optimization

## Purpose
To improve the rendering performance of React applications by preventing unnecessary re-renders of components.

## When to Use
- When a component renders often (e.g., list items, inputs).
- When a component receives complex props (objects/arrays).
- When profiling reveals "wasted renders".

## Procedure
1.  **Identify Bottlenecks**: Use React DevTools Profiler to find components rendering too frequently.
2.  **Memoize Component**: Wrap the component export with `React.memo()`.
    - `export const MyComponent = React.memo(function MyComponent(props) { ... });`
3.  **Memoize Props**:
    - Use `useCallback` for functions passed as props: `const handleClick = useCallback(() => { ... }, [deps])`.
    - Use `useMemo` for expensive calculations or object/array props: `const data = useMemo(() => ({ id }), [id])`.
4.  **Virtualize Lists**: If the list is huge, use `react-window` or `react-virtualized` to render only visible items.

## Constraints
- Do not memoize everything blindly; it adds overhead. Only optimize where needed.
- Ensure dependency arrays in hooks are correct (use lint rules).

## Expected Output
A component structure that only re-renders when its specific props or state actually change, resulting in a smoother UI.

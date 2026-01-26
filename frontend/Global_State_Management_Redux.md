# Skill: Global State Management (Redux Toolkit)

## Purpose
To manage shared state across the application predictably, avoiding "prop drilling" and complex context hierarchies.

## When to Use
- When state is needed by many components at different nesting levels (e.g., User, Theme, Cart).
- When state logic is complex (many actions updating same data).

## Procedure
1.  **Create Slice**: Define a "slice" using `createSlice`.
    - Name the slice.
    - Define `initialState`.
    - Define `reducers` (functions to mutate state).
2.  **Configure Store**: Use `configureStore` to combine slice reducers.
3.  **Provide Store**: Wrap the root App component with `<Provider store={store}>`.
4.  **Consume State**: Use `useSelector` to read data: `const user = useSelector(state => state.user)`.
5.  **Dispatch Actions**: Use `useDispatch` to trigger changes: `dispatch(increment())`.

## Constraints
- Do not put *everything* in Redux. Local UI state (like form inputs, modal open/close) should often stay local.
- Keep state serializable (no functions or classes in store).

## Expected Output
A Redux store setup with typed slices, actions, and selectors ready for consumption by components.

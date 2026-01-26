# Skill: API Data Fetching (TanStack Query)

## Purpose
To handle server state (fetching, caching, synchronizing, and updating) in React applications, replacing manual `useEffect` fetching logic.

## When to Use
- Fetching data from REST or GraphQL APIs.
- When you need caching, deduplication, background updates, or optimistic UI.

## Procedure
1.  **Setup Provider**: Wrap app in `QueryClientProvider`.
2.  **Create Query**: Use `useQuery`.
    - Key: Unique array `['todos', { status }]`.
    - Fetcher: Async function returning data.
    - `const { data, isLoading, error } = useQuery({ queryKey: [...], queryFn: fetchTodos })`.
3.  **Create Mutation**: Use `useMutation` for POST/PUT/DELETE.
    - `const mutation = useMutation({ mutationFn: addTodo })`.
4.  **Invalidate**: On mutation success, invalidate query to refetch fresh data: `queryClient.invalidateQueries({ queryKey: ['todos'] })`.

## Constraints
- Define query keys consistently.
- Handle loading and error states explicitly in the UI.
- Do not use for local synchronous state (use `useState` or Redux).

## Expected Output
A data-fetching layer that automatically handles loading states, caching, and re-validation, reducing boilerplate significantly.

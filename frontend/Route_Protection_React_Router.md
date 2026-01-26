# Skill: Route Protection (React Router)

## Purpose
To restrict access to specific pages (routes) based on user authentication status or roles, redirecting unauthorized users.

## When to Use
- Dashboards, settings pages, or any private content.
- Redirecting logged-in users away from Login/Signup pages.

## Procedure
1.  **Create Wrapper**: Create a `ProtectedRoute` component.
    - Props: `children` (the page to render).
2.  **Check Auth**: Read auth state (from Context/Redux).
3.  **Conditional Render**:
    - If `isAuthenticated`, return `children`.
    - If not, return `<Navigate to="/login" replace />`.
4.  **Usage**: Wrap routes in the router definition.
    - `<Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />`.
5.  **Role Check** (Optional): Extend to check `user.role` for admin routes.

## Constraints
- Always handle the "loading" state of authentication (don't redirect while checking if the user is logged in).
- Remember: Client-side protection is UX only; the API must still be secured.

## Expected Output
A routing configuration that automatically guards private pages and handles redirects for unauthenticated users.

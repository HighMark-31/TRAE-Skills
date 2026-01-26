# Skill: RBAC Implementation (Role-Based Access Control)

## Purpose
To restrict access to specific API resources based on the user's assigned role (e.g., Admin, Editor, User).

## When to Use
- When different users have different permission levels.
- When protecting administrative endpoints.

## Procedure
1.  **Define Roles**: Enum or database table (e.g., `['admin', 'manager', 'user']`).
2.  **Assign Roles**: Store `role` on the User entity.
3.  **Create Middleware**:
    - Factory function `restrictTo(...allowedRoles)`.
    - Check `req.user.role`.
    - If `allowedRoles.includes(user.role)`, call `next()`.
    - Else, return 403 Forbidden.
4.  **Apply to Routes**: Add middleware after authentication: `router.delete('/users/:id', auth, restrictTo('admin'), controller.deleteUser)`.
5.  **Granular Permissions** (Optional): Map roles to specific permissions (e.g., `can_delete_user`) for complex systems.

## Constraints
- Fail closed (default to no access).
- Don't rely on frontend hiding; always enforce on backend.
- Hierarchical roles (Admin > Manager) require logic to check "at least" that role.

## Expected Output
A middleware that enforces role boundaries, ensuring users cannot perform actions outside their privilege level.

# Skill: Advanced RBAC (Role-Based Access Control)

## Purpose
To implement a scalable permission system where users have roles, and roles have granular permissions.

## When to Use
- B2B SaaS applications (Admin, Editor, Viewer).
- Systems with complex access requirements.

## Procedure

### 1. Data Model
- **Users**: `id`, `name`, `role_id` (or m:n `user_roles`).
- **Roles**: `id`, `name` (e.g., 'admin', 'editor').
- **Permissions**: `id`, `action`, `resource` (e.g., `create:post`, `read:user`).
- **RolePermissions**: Join table.

### 2. Middleware (Enforcement)
Don't check roles (`if user.role === 'admin'`). **Check permissions**.
```javascript
// middleware/authorize.js
const authorize = (requiredPermission) => {
  return async (req, res, next) => {
    const userPermissions = await getUserPermissions(req.user.id); // Cached in JWT or Redis
    if (!userPermissions.includes(requiredPermission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
};

// usage
app.post('/posts', authorize('create:post'), createPost);
```

### 3. Hierarchy (Optional)
Roles can inherit from others.
- `Admin` has all permissions of `Editor` + `delete:user`.
- This logic is handled in the permission resolution function.

### 4. Frontend Integration
Send permissions list to frontend on login.
```javascript
{
  token: "...",
  user: {
    id: 1,
    permissions: ["read:posts", "create:posts"]
  }
}
```
Use a `<Can permission="create:posts">` component to hide/show UI elements.

## Constraints
- **Granularity**: Balance between too broad (`manage:all`) and too specific (`update:post:title`).
- **Caching**: Fetching permissions on every request is slow. Cache them in the JWT or Redis (invalidate on role change).

## Expected Output
A flexible security model allowing admins to configure what users can do without changing code.

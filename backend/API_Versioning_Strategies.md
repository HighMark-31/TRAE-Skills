# Skill: API Versioning Strategies

## Purpose
To manage changes in API contracts without breaking existing clients, ensuring backward compatibility.

## When to Use
- When introducing breaking changes (renaming fields, changing data types, removing endpoints).
- When supporting mobile apps that cannot be forced to update immediately.

## Procedure

### 1. URI Versioning (Most Common)
Include version in the path. Clear and cache-friendly.
- `GET /api/v1/users`
- `GET /api/v2/users`

Implementation (Express):
```javascript
const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

### 2. Header Versioning
Cleaner URLs, but harder to test via browser.
- Header: `Accept-Version: v1`

Implementation:
```javascript
app.get('/users', (req, res) => {
  const version = req.get('Accept-Version');
  if (version === 'v2') return handlerV2(req, res);
  return handlerV1(req, res);
});
```

### 3. Query Parameter
Easy for debugging.
- `GET /api/users?version=1`

### 4. Deprecation Strategy
1.  **Announce**: Mark fields/endpoints as deprecated in docs.
2.  **Sunset Header**: Add `Sunset: <Date>` header to responses indicating when the version will be removed.
3.  **Brownouts**: Intentionally fail requests for short periods as EOL approaches to alert developers.

## Constraints
- **Code Duplication**: Managing multiple versions can lead to duplicated logic. Use "Controller-Service" pattern to share business logic where possible, applying adapters for the response format.
- **Maintenance**: Limit supported versions (e.g., maintain only the last 2 major versions).

## Expected Output
A stable API ecosystem where clients can upgrade at their own pace without service interruption.

# Skill: API REST Endpoint Design

## Purpose
To design and implement a RESTful API endpoint that is consistent, scalable, and follows industry best practices for HTTP methods, status codes, and URL structure.

## When to Use
- When creating a new API resource or sub-resource.
- When refactoring existing endpoints to meet REST standards.
- When defining the contract between frontend and backend.

## Procedure
1.  **Identify Resource**: Determine the noun representing the resource (e.g., `/users`, `/orders`). Use plural nouns.
2.  **Select HTTP Method**:
    - `GET` for retrieval.
    - `POST` for creation.
    - `PUT` for full replacement.
    - `PATCH` for partial update.
    - `DELETE` for removal.
3.  **Define URL Structure**:
    - Use hierarchy: `/resources/{id}/sub-resources`.
    - Avoid verbs in URLs (e.g., use `POST /users/login` only if `session` is the resource, otherwise standard RPC might be an exception, but prefer REST).
4.  **Define Request Payload**:
    - Specify JSON body structure for POST/PUT/PATCH.
    - Define query parameters for GET (filtering, pagination, sorting).
5.  **Define Response Structure**:
    - Standardize success response (e.g., `{ data: ... }`).
    - Standardize error response (e.g., `{ error: { code: ..., message: ... } }`).
6.  **Select Status Codes**:
    - 200 (OK), 201 (Created), 204 (No Content).
    - 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found).
    - 500 (Internal Server Error).

## Constraints
- Do NOT expose internal database IDs if UUIDs are available/preferred.
- Do NOT mix snake_case and camelCase in JSON responses (prefer camelCase for JS/Node).
- Ensure all endpoints are stateless.

## Expected Output
A fully defined route handler (or controller method) with request validation, business logic invocation, and a standardized JSON response.

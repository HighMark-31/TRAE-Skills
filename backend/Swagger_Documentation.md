# Skill: Swagger Documentation Generation

## Purpose
To automatically generate interactive API documentation that stays up-to-date with the codebase, aiding frontend developers and third-party integrators.

## When to Use
- When exposing APIs to other teams or the public.
- When strictly defining API contracts.
- When standardizing API development.

## Procedure
1.  **Install Tools**: `swagger-jsdoc` and `swagger-ui-express`.
2.  **Configure Definition**: Create a `swaggerDef.js` or equivalent config with API meta-info (title, version, server URL).
3.  **Annotate Code**:
    - Add JSDoc/YAML comments above route handlers describing:
        - Path and Method.
        - Parameters and Request Body.
        - Response Codes and Schemas.
    - Alternatively, use a library that infers docs from validation schemas (e.g., `zod-to-openapi`).
4.  **Mount UI**: Add a route (e.g., `/api-docs`) to serve the Swagger UI using the generated spec.
5.  **Secure Docs**: Protect the documentation route if the API is private.

## Constraints
- Documentation must match the actual implementation.
- Keep schemas reusable (use `$ref` definitions).
- Do not expose sensitive internal endpoints in public documentation.

## Expected Output
A live `/api-docs` endpoint displaying interactive Swagger UI, generated from code annotations or schemas.

# Skill: Input Validation (Zod)

## Purpose
To validate incoming request data (body, query, params) against a strict schema before processing it, ensuring type safety and data integrity.

## When to Use
- When accepting any user input.
- When defining TypeScript interfaces for API requests.
- When preventing injection attacks and malformed data issues.

## Procedure
1.  **Define Schema**: Create a Zod schema defining the expected shape (e.g., `z.object({ email: z.string().email() })`).
2.  **Infer Type**: Export the TypeScript type from the schema (`type CreateUserDto = z.infer<typeof UserSchema>`).
3.  **Create Middleware**:
    - Write a middleware that accepts a schema.
    - In the middleware, run `schema.parse(req.body)`.
    - If valid, replace `req.body` with the parsed (sanitized) data.
    - If invalid, catch the ZodError and return a 400 Bad Request with detailed field errors.
4.  **Attach to Route**: Add the middleware before the controller.

## Constraints
- Validate "strip unknown" to prevent pollution (Zod does this by default with `.parse()`, or explicit `.strict()`).
- Validate data types, formats (email, uuid), and lengths.
- Do not trust client-side validation alone.

## Expected Output
A robust validation layer that rejects invalid requests early and provides typed request bodies to controllers.

# Skill: Express Middleware Creation

## Purpose
To create reusable Express.js middleware functions for cross-cutting concerns such as logging, authentication, validation, or request preprocessing.

## When to Use
- When logic needs to be applied to multiple routes or the entire application.
- When processing headers, cookies, or body parsing before the controller.
- When attaching custom properties to the `req` object (e.g., `req.user`).

## Procedure
1.  **Define Function Signature**: Create a function accepting `(req, res, next)`.
2.  **Implement Logic**:
    - Perform the specific task (e.g., check header, parse token).
    - Handle errors: If an error occurs, pass it to `next(err)`.
3.  **Control Flow**:
    - If the request should proceed, call `next()`.
    - If the request should stop (e.g., validation failure), send a response (e.g., `res.status(400).json(...)`) and do NOT call `next()`.
4.  **Context Attachment**: If needed, attach data to `req` (e.g., `req.currentUser = decodedToken`).
5.  **Export**: Export the function for use in routes or `app.use()`.

## Constraints
- Always call `next()` or send a response; otherwise, the request will hang.
- Do not perform heavy blocking synchronous operations in middleware.
- Error handling middleware must have 4 arguments: `(err, req, res, next)`.

## Expected Output
A standalone JavaScript/TypeScript file exporting a middleware function that can be mounted in an Express application.

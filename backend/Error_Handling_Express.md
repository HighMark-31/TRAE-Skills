# Skill: Error Handling (Express)

## Purpose
To implement a centralized error handling mechanism in Express applications that captures synchronous and asynchronous errors, logs them properly, and sends standardized responses to the client.

## When to Use
- When setting up the application structure.
- When refactoring to remove `try/catch` boilerplate in controllers.
- When ensuring consistent API error responses.

## Procedure
1.  **Create Custom Error Classes**: Extend `Error` (e.g., `AppError`) with properties for `statusCode` and `isOperational`.
2.  **Create Error Middleware**: Define a function with signature `(err, req, res, next)`.
3.  **Handle Known Errors**:
    - Check if `err` is an instance of `AppError`.
    - Use `err.statusCode` and `err.message`.
4.  **Handle Unknown Errors**:
    - Log the full error stack (for developers/logs).
    - Send a generic 500 "Internal Server Error" message to the client (security).
5.  **Async Wrapper**: Create a helper function (e.g., `catchAsync`) to wrap async route handlers and automatically pass errors to `next()`.
6.  **Register Middleware**: Place the error handler as the *last* middleware in `app.js`.

## Constraints
- Never expose stack traces in production responses.
- Differentiate between operational errors (invalid input) and programming errors (bugs).
- Ensure all async routes are wrapped or use Express 5+ (which handles rejected promises).

## Expected Output
A robust error handling infrastructure including custom error classes, an error handling middleware, and an async wrapper utility.

# Skill: Logger Configuration (Winston)

## Purpose
To implement a structured logging system that outputs JSON logs for machine parsing (in production) and readable text (in development), aiding in debugging and monitoring.

## When to Use
- When replacing `console.log` statements.
- When setting up observability tools (ELK stack, Datadog, etc.).
- When needing different log levels (INFO, WARN, ERROR).

## Procedure
1.  **Install Winston**: `npm install winston`.
2.  **Create Logger Instance**:
    - Configure transports: `Console` (standard).
    - Configure format:
        - Development: `format.combine(format.colorize(), format.simple())`.
        - Production: `format.combine(format.timestamp(), format.json())`.
3.  **Define Levels**: Use standard syslog levels (Error, Warn, Info, HTTP, Verbose, Debug, Silly).
4.  **Create Wrapper**: Export the logger instance.
5.  **Integrate with Express**: Use `morgan` or a custom middleware to pipe HTTP requests into the Winston logger.
6.  **Usage**: Replace `console.log` with `logger.info()`, `logger.error()`, etc.

## Constraints
- Do not log sensitive data (passwords, tokens, PII).
- Ensure logs include context (trace ID, user ID) where possible.
- Use correct log levels (don't log errors as info).

## Expected Output
A centralized logger module that outputs structured JSON logs in production and colored text in development.

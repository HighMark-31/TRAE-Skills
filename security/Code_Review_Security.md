# Skill: Code Review Security Checklist

## Purpose
To systematically review code changes for common security flaws before merging, preventing vulnerabilities from reaching production.

## When to Use
- During every Pull Request (PR) review.
- When auditing legacy code.

## Procedure
1.  **Injection**: Check for raw SQL queries or unescaped HTML output. Ensure parameterized queries/ORM and sanitization are used.
2.  **Authentication/AuthZ**:
    - Are protected routes actually checking the user's role/token?
    - Is the user allowed to access the specific resource ID (IDOR check)?
3.  **Data Exposure**:
    - Are passwords/secrets logged?
    - Are internal implementation details (stack traces) exposed in API errors?
4.  **Input Validation**: Is all user input (body, params, query) validated against a schema?
5.  **Dependencies**: Did the PR introduce a new package? Is it reputable and necessary?

## Constraints
- Don't just look for logic bugs; actively look for security holes.
- Assume all input is malicious.
- Verify that "safe" defaults are used.

## Expected Output
A completed review comment or approval indicating that specific security aspects have been verified.

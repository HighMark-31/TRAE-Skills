# Skill: Secure Environment Variable Handling

## Purpose
To manage configuration and sensitive secrets securely, preventing hardcoded credentials and ensuring consistency across environments.

## When to Use
- When adding API keys, database URLs, secrets, or configuration flags.
- When setting up a new project or deployment environment.

## Procedure
1.  **Identify Secrets**: Determine which values are sensitive (passwords, keys) or environment-specific (URLs, ports).
2.  **Update `.env.example`**: Add the key name (e.g., `DB_HOST=`) to the example file without the real value.
3.  **Configure `.gitignore`**: Ensure `.env` and `*.env` files are ignored to prevent committing secrets.
4.  **Load Variables**: Use a library like `dotenv` (in Node.js) to load variables at app startup.
5.  **Type/Validate Config**: Create a configuration module that reads `process.env`, validates presence/format (e.g., using `envalid` or `zod`), and exports a typed config object.
6.  **Usage**: Replace hardcoded values in code with the exported config object properties.

## Constraints
- NEVER commit real secrets to version control.
- Do not access `process.env` directly in business logic; use the centralized config module.
- Ensure variable names are uppercase with underscores (SCREAMING_SNAKE_CASE).

## Expected Output
An updated `.env.example`, a specific `.env` file (local only), and a configuration module (e.g., `src/config/index.ts`) that validates and exports the settings.

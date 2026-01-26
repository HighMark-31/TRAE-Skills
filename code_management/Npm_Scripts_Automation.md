# NPM Scripts Automation

## Overview
Use `package.json` scripts to standardize common development tasks.

## Best Practices
- **Naming**: Use standard names like `start`, `build`, `test`.
- **Composition**: Use `pre` and `post` hooks (e.g., `prebuild` runs before `build`).
- **Cross-platform**: Use tools like `rimraf` for deletion and `cross-env` for environment variables to ensure scripts work on Windows and Unix.

## Example
```json
"scripts": {
  "start": "node dist/index.js",
  "dev": "nodemon src/index.ts",
  "build": "tsc",
  "lint": "eslint .",
  "test": "jest"
}
```

# ESLint & Prettier Setup

## Overview
Consistent code style and catching errors early are essential for maintainability.

## Implementation
1. **Install**:
   ```bash
   npm install --save-dev eslint prettier
   ```
2. **Config**:
   - Create `.eslintrc.json` or `eslint.config.js`.
   - Create `.prettierrc`.
3. **Integration**:
   - Use `eslint-config-prettier` to disable ESLint rules that conflict with Prettier.

## Usage
- Run `eslint . --fix` to auto-fix linting issues.
- Run `prettier --write .` to format code.

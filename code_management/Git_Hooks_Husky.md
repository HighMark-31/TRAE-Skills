# Git Hooks with Husky

## Overview
Automate tasks like linting and testing before commits or pushes to ensure code quality.

## Setup
1. **Install Husky**:
   ```bash
   npm install --save-dev husky
   npx husky install
   ```
2. **Add Hook**:
   ```bash
   npx husky add .husky/pre-commit "npm run lint"
   ```

## Common Hooks
- `pre-commit`: Run linter, type check.
- `commit-msg`: Verify commit message format (e.g., using commitlint).
- `pre-push`: Run unit tests.

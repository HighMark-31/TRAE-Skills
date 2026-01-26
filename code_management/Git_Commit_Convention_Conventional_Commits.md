# Git Commit Convention (Conventional Commits)

## Overview
Standardizing commit messages is crucial for automated changelog generation and clear project history.

## Best Practices
- **Format**: `type(scope): subject`
- **Types**:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation only
  - `style`: Formatting, missing semi colons, etc; no code change
  - `refactor`: Refactoring production code
  - `test`: Adding tests, refactoring test; no production code change
  - `chore`: Updating build tasks, package manager configs, etc

## Example
```bash
git commit -m "feat(auth): implement jwt token handling"
```

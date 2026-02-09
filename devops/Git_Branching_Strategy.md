# Skill: Git Branching Strategy (GitFlow/Trunk)

## Purpose
To standardize how developers collaborate on code, manage releases, and handle hotfixes to avoid conflicts and chaotic history.

## When to Use
- Setting up a new team workflow.
- Solving "merge hell" situations.

## Procedure

### 1. Trunk-Based Development (Recommended for CI/CD)
The most efficient workflow for modern DevOps teams.

```bash
# 1. Create a short-lived feature branch from main
git checkout main
git pull origin main
git checkout -b feature/user-auth-api

# 2. Commit frequently with descriptive messages
git add .
git commit -m "feat: add jwt validation middleware"

# 3. Push and open a Pull Request (PR)
git push origin feature/user-auth-api

# 4. After PR approval and CI pass, merge to main (Squash merge preferred)
# (Done via GitHub/GitLab UI)

# 5. Delete local and remote branch
git branch -d feature/user-auth-api
git push origin --delete feature/user-auth-api
```

### 2. Standardized Naming Convention
Use prefixes to categorize branches and commits.

- **`feat/`**: New feature development.
- **`fix/`**: Bug fix for the current environment.
- **`hotfix/`**: Critical fix for production.
- **`chore/`**: Maintenance tasks (updating dependencies, etc.).
- **`docs/`**: Documentation changes only.
- **`refactor/`**: Code change that neither fixes a bug nor adds a feature.

### 3. Release Management
Use Git Tags to mark production releases.

```bash
# Create a semantic version tag
git tag -a v1.2.0 -m "Release version 1.2.0: Includes User Auth and Billing fixes"

# Push tags to remote
git push origin v1.2.0
```

### 4. Handling Conflicts
Rebase or merge from main frequently to minimize conflict size.

```bash
# Bring latest changes from main into your branch
git checkout feature/my-feature
git fetch origin
git rebase origin/main

# If conflicts occur:
# 1. Manually fix files in editor
# 2. git add <fixed-files>
# 3. git rebase --continue
```

## Constraints
- **Branch Longevity**: Feature branches should not live longer than 2-3 days. Long-lived branches lead to complex merge conflicts.
- **Protected Branches**: Enable branch protection on `main` or `develop`. Require at least one approval and passing CI status before merging.
- **Commit History**: Use "Squash and Merge" for PRs to keep the `main` history clean and linear.
- **No Direct Pushes**: Never allow direct pushes to protected branches; everything must go through a PR.

## Expected Output
A documented workflow policy that the team follows for all code changes.

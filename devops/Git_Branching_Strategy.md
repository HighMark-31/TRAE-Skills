# Skill: Git Branching Strategy (GitFlow/Trunk)

## Purpose
To standardize how developers collaborate on code, manage releases, and handle hotfixes to avoid conflicts and chaotic history.

## When to Use
- Setting up a new team workflow.
- Solving "merge hell" situations.

## Procedure
1.  **Choose Model**:
    - **Trunk-Based**: Main branch is always deployable. Short-lived feature branches merge to main. (Best for CI/CD, fast pace).
    - **GitFlow**: `develop` for integration, `master` for prod, `release/*` for stabilization, `hotfix/*` for urgent fixes. (Good for versioned software).
2.  **Rules**:
    - Never push directly to `main`/`master`.
    - Use Pull Requests (PRs) for code review.
    - Require CI checks to pass before merging.
3.  **Naming Conventions**: `feature/login-page`, `bugfix/header-crash`, `hotfix/prod-500`.
4.  **Tagging**: Tag releases (`v1.0.0`) in Git.

## Constraints
- Keep branches short-lived (merge often).
- Resolve conflicts immediately.
- Delete branches after merging.

## Expected Output
A documented workflow policy that the team follows for all code changes.

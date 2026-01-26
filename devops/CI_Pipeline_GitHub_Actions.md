# Skill: CI Pipeline Setup (GitHub Actions)

## Purpose
To automate the testing, building, and linting process whenever code is pushed, ensuring quality control before merging.

## When to Use
- When setting up a new repository.
- When enforcing code quality standards automatically.
- When automating deployment (CD) steps.

## Procedure
1.  **Create Workflow File**: Create `.github/workflows/ci.yml`.
2.  **Define Triggers**: Set `on: [push, pull_request]` for main/develop branches.
3.  **Define Jobs**:
    - **Lint**: Checkout code, install deps, run `npm run lint`.
    - **Test**: Checkout code, install deps, run `npm test`.
    - **Build**: Checkout code, install deps, run `npm run build`.
4.  **Configure Environment**: Use `strategy.matrix` to test across Node.js versions if necessary.
5.  **Cache Dependencies**: Use `actions/setup-node` with caching enabled to speed up builds.

## Constraints
- Fail the pipeline if any step fails.
- Do not expose secrets in logs (use GitHub Secrets).
- Ensure tests run in an environment that mimics production (e.g., use service containers for databases).

## Expected Output
A `.github/workflows/ci.yml` file that triggers on push/PR and successfully executes linting, testing, and building tasks.

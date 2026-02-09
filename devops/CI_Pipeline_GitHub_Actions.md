# Skill: CI Pipeline Setup (GitHub Actions)

## Purpose
To automate the testing, building, and linting process whenever code is pushed, ensuring quality control and preventing regressions before merging.

## When to Use
- When setting up a new repository.
- When enforcing code quality standards (Lint, Prettier).
- When automating deployment (CD) or release management.

## Procedure

### 1. Workflow Configuration (Node.js)
Create `.github/workflows/ci.yml` in your repository.

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm' # Speeds up builds by caching node_modules

      - name: Install Dependencies
        run: npm ci

      - name: Run Lint
        run: npm run lint

      - name: Run Tests
        run: npm test -- --coverage

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

### 2. Handling Environment Secrets
Never hardcode secrets. Use GitHub Repository Secrets.

```yaml
      - name: Run Integration Tests
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          TEST_API_KEY: ${{ secrets.TEST_API_KEY }}
        run: npm run test:integration
```

### 3. Service Containers (Databases)
Run a database alongside your tests using Docker services.

```yaml
    services:
      redis:
        image: redis
        ports:
          - 6379:6379
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: password
        ports:
          - 5432:5432
```

### 4. Build Artifacts
Save build outputs for later deployment stages.

```yaml
      - name: Build Application
        run: npm run build

      - name: Upload Build Artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
```

## Constraints
- **Security**: Do not log sensitive environment variables. Use masked secrets.
- **Efficiency**: Use caching for `npm` or `yarn` to keep build times under 5 minutes.
- **Reliability**: Ensure tests run in a clean environment every time.

## Expected Output
A fully functional GitHub Action that automatically validates every pull request and push to protected branches.

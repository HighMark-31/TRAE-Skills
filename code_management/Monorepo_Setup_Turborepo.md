# Monorepo Setup (Turborepo)

## Overview
Managing multiple packages or apps in a single repository can simplify dependency management and code sharing.

## Key Concepts
- **Workspaces**: NPM/Yarn/PNPM workspaces to link packages locally.
- **Turborepo**: High-performance build system for monorepos.

## Procedure

### 1. Workspace Configuration
Define your project structure in `package.json` (for NPM/Yarn) or `pnpm-workspace.yaml`.

```json
// package.json (root)
{
  "workspaces": [
    "apps/*",
    "packages/*"
  ]
}
```

### 2. Initialize Turborepo
Add Turbo to your project.

```bash
npx init turbo@latest
```

### 3. Configuring `turbo.json`
Define the dependency graph and cacheable tasks.

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"], // Build dependencies first
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {}
  }
}
```

### 4. Running Commands
Turbo automatically parallelizes tasks and caches results.

```bash
# Build all apps and packages
npx turbo run build

# Run tests only for changed packages
npx turbo run test --filter=...[origin/main]
```

## Constraints
- **Circular Dependencies**: Avoid circular dependencies between packages in the monorepo.
- **Hoisting**: Be aware of how dependencies are "hoisted" to the root `node_modules`.
- **Versioning**: Decide between a "Fixed" versioning strategy (all packages same version) or "Independent" versioning.

## Expected Output
A high-performance monorepo where builds and tests are optimized through intelligent caching and parallel execution.

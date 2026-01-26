# Monorepo Setup (Turborepo)

## Overview
Managing multiple packages or apps in a single repository can simplify dependency management and code sharing.

## Key Concepts
- **Workspaces**: NPM/Yarn/PNPM workspaces to link packages locally.
- **Turborepo**: High-performance build system for monorepos.

## Structure
```
/apps
  /web
  /docs
/packages
  /ui
  /utils
  /tsconfig
```

## Benefits
- Atomic commits across projects.
- Shared configuration (ESLint, TSConfig).
- Faster builds with caching.

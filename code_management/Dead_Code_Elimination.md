# Dead Code Elimination

## Overview
Removing unused code reduces bundle size and maintenance burden.

## Techniques
1. **Tree Shaking**: Ensure your bundler (Webpack, Rollup, Vite) is configured to remove unused exports.
2. **Tools**:
   - `knip`: Finds unused files and exports.
   - `ts-prune`: Finds unused exports in TypeScript projects.
3. **Regular Audits**: Periodically check for deprecated features or unused components.

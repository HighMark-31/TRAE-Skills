# Dead Code Elimination

## Overview
Removing unused code reduces bundle size and maintenance burden.

## Procedure

### 1. Automated Detection (Knip)
Knip is a powerful tool to find unused files, dependencies, and exports.

```bash
# Install
npm install --save-dev knip

# Run analysis
npx knip
```

### 2. TypeScript-Specific Audit (ts-prune)
Find unused exports in your TypeScript files.

```bash
# Run directly with npx
npx ts-prune | grep -v "(used in module)"
```

### 3. Bundler Tree Shaking
Ensure your `package.json` and bundler config (Vite/Webpack) support tree shaking.
- Set `"sideEffects": false` in `package.json` for libraries that don't have side effects.
- Use ES Modules (`import/export`) instead of CommonJS (`require`).

### 4. Manual Review
- **Search for Usage**: Before deleting, use `grep` or IDE search to verify no dynamic references exist.
- **Delete and Test**: Delete the code, run the full test suite, and check for runtime errors.

## Constraints
- **Side Effects**: Be careful with code that has side effects (e.g., global polyfills, CSS imports).
- **Dynamic Access**: Tools might miss code accessed via dynamic strings (e.g., `eval` or `object[someVar]`).
- **Dependencies**: Don't just delete code; also remove unused packages from `package.json` (`npm uninstall`).

## Expected Output
A leaner codebase with reduced bundle sizes, faster build times, and less "noise" for developers to maintain.

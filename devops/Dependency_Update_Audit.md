# Skill: Dependency Update Audit

## Purpose
To regularly check, update, and audit project dependencies for security vulnerabilities and deprecations, maintaining a healthy codebase.

## When to Use
- On a scheduled basis (e.g., monthly).
- When a security advisory is released.
- Before major feature development cycles.

## Procedure
1.  **Check Outdated**: Run `npm outdated` to see available updates.
2.  **Audit Security**: Run `npm audit` to identify vulnerabilities.
3.  **Update Minor/Patch**:
    - Run `npm update` to respect semver ranges in `package.json`.
    - Verify app functionality (run tests).
4.  **Update Major**:
    - Read changelogs for breaking changes.
    - Update one major dependency at a time.
    - Fix breaking changes and run full test suite.
5.  **Lockfile**: Commit the updated `package-lock.json`.

## Constraints
- Do not blindly update all packages at once, especially major versions.
- Pin exact versions if a package is known to be unstable.
- Fix `npm audit` critical/high vulnerabilities immediately.

## Expected Output
An updated `package.json` and `package-lock.json` with fewer vulnerabilities and up-to-date libraries.

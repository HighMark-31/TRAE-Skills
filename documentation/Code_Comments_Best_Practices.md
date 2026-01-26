# Code Comments Best Practices

## Overview
Comments should explain *why*, not *what*. The code itself should explain *what*.

## Guidelines
- **Self-Documenting Code**: Prefer clear variable/function names over comments.
- **Docstrings**: Use JSDoc/TSDoc for functions and classes (params, returns).
- **TODOs**: Mark incomplete work with `TODO` or `FIXME`.
- **Avoid**:
  - Commented-out code (just delete it, git has history).
  - Redundant comments (`i++; // increment i`).

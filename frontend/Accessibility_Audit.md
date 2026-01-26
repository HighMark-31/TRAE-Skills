# Skill: Accessibility (a11y) Audit

## Purpose
To ensure the application is usable by people with disabilities, complying with WCAG standards and improving SEO/UX.

## When to Use
- During development of UI components.
- Before major releases.

## Procedure
1.  **Semantic HTML**: Use correct tags (`<button>` vs `<div>`, `<nav>`, `<main>`).
2.  **Keyboard Navigation**: Ensure all interactive elements are focusable and usable via Tab/Enter/Space.
3.  **ARIA Labels**: Add `aria-label` or `aria-labelledby` where text is missing (icons).
4.  **Color Contrast**: Check text vs background contrast ratio (aim for AA standard).
5.  **Alt Text**: Ensure all meaningful images have `alt` attributes.
6.  **Tools**:
    - Run `Lighthouse` audit in Chrome DevTools.
    - Use `eslint-plugin-jsx-a11y` to catch issues while coding.

## Constraints
- Do not use `tabindex` greater than 0.
- Do not rely on color alone to convey information (use icons/text too).

## Expected Output
A report of accessibility issues and a refactored UI that passes automated a11y checks.

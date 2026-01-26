# Skill: Responsive UI Design (Tailwind CSS)

## Purpose
To create user interfaces that adapt seamlessly to different screen sizes (Mobile, Tablet, Desktop) using a utility-first CSS framework.

## When to Use
- Building any user-facing layout.
- Ensuring mobile compatibility.

## Procedure
1.  **Mobile First**: Design for the smallest screen first (default classes).
    - `<div class="block">` (Mobile default).
2.  **Add Breakpoints**: Use prefixes (`sm:`, `md:`, `lg:`, `xl:`) to override styles on larger screens.
    - `<div class="block md:flex">` (Block on mobile, Flex on tablet+).
3.  **Grid/Flex Layouts**:
    - Use `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` for responsive grids.
4.  **Spacing/Typography**: Adjust padding and font size for readability on different devices.
    - `p-4 md:p-8`, `text-sm md:text-base`.

## Constraints
- Do not use fixed widths (`w-96`) unless necessary; use percentages or `max-w` containers.
- Test on actual devices or DevTools device mode, not just resizing the browser window.

## Expected Output
A UI component that looks and functions correctly across a range of device viewports.

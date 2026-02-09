# Skill: Mobile-First Design

## Purpose
To design and develop UIs starting with the smallest screen sizes (mobile) and progressively enhancing for larger screens (tablet, desktop).

## When to Use
- All responsive web projects.
- To ensure core content is prioritized.

## Procedure

### 1. CSS Media Queries (Min-Width)
Write base styles for mobile first (no query). Add overrides for larger screens.
```css
/* Mobile (Base) */
.container {
  padding: 10px;
  font-size: 14px;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 20px;
    font-size: 16px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
    margin: 0 auto;
  }
}
```

### 2. Tailwind CSS approach
Tailwind is mobile-first by default.
`<div class="p-4 md:p-8 lg:max-w-4xl">`
- `p-4`: Applies to all.
- `md:p-8`: Applies to 768px+.

### 3. Layout Patterns
- **Stack to Row**: Flex-direction column on mobile, row on desktop.
- **Hamburger Menu**: Hidden on desktop, visible on mobile.
- **Touch Targets**: Buttons must be at least 44x44px for touch.

## Constraints
- **Testing**: Constantly resize browser or use DevTools Device Mode. Don't assume desktop view is the "default".
- **Hover**: Mobile devices don't have hover states. Do not hide critical functionality behind hover.

## Expected Output
A responsive interface that is performant on mobile devices and utilizes available space on desktops.

# Skill: SVG Animation Techniques

## Purpose
To create scalable, crisp animations for icons, logos, and illustrations using CSS or JavaScript libraries.

## When to Use
- Loading spinners.
- Interactive icons (hamburger menu to X).
- Complex illustrations (paths drawing themselves).

## Procedure

### 1. CSS Animation (Simple)
Manipulate properties like `opacity`, `transform`, `stroke-dasharray`.
```css
/* Draw a line effect */
.path {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: draw 2s forwards;
}

@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```

### 2. SMIL (Native SVG)
Using `<animate>` tags inside SVG. Deprecated in some contexts but powerful.
```xml
<circle cx="50" cy="50" r="40">
  <animate attributeName="cx" from="50" to="150" dur="1s" repeatCount="indefinite" />
</circle>
```

### 3. GSAP (GreenSock) - Standard for Complex Motion
Robust, cross-browser, high performance.
```javascript
import gsap from 'gsap';

gsap.to(".box", { 
  rotation: 360, 
  x: 100, 
  duration: 1 
});
```

### 4. Framer Motion (React)
Declarative animations.
```tsx
<motion.path
  initial={{ pathLength: 0 }}
  animate={{ pathLength: 1 }}
/>
```

## Constraints
- **Complexity**: Animating many DOM nodes/SVG elements can cause layout thrashing.
- **Optimization**: Optimize SVGs (SVGO) before animating to remove useless metadata and group elements properly.

## Expected Output
Smooth, resolution-independent animations that enhance UI interactivity.

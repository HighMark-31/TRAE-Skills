# Skill: Handling Large Lists (Virtualization)

## Purpose
To render large datasets (thousands of items) efficiently by only rendering the items currently visible in the viewport (Windowing).

## When to Use
- Infinite scroll feeds.
- Large data tables.
- Chat history logs.

## Procedure

### 1. Concept
Instead of rendering 10,000 `<div>`s, calculate which 10 fit in the screen based on scroll position and render only those (plus a buffer).

### 2. Libraries
- **React**: `react-window` (Lightweight) or `react-virtualized` (Feature-rich).
- **TanStack Virtual**: Framework agnostic.

### 3. Implementation (react-window)
```bash
npm install react-window
```

```tsx
import { FixedSizeList as List } from 'react-window';

const Row = ({ index, style }) => (
  <div style={style}>Row {index}</div>
);

const Example = () => (
  <List
    height={500} // Viewport height
    itemCount={1000}
    itemSize={35} // Row height
    width={300}
  >
    {Row}
  </List>
);
```

### 4. Dynamic Heights
If items vary in height, use `VariableSizeList` and provide a function `getItemSize(index)`. This requires measuring content (more complex).

## Constraints
- **SEO**: Virtualized content is not in the DOM until scrolled. Search engines might not see it. (Use server-side rendering or "Load More" for SEO critical content).
- **Scrolling**: "Ctrl+F" browser search breaks because items don't exist in DOM.

## Expected Output
Smooth scrolling (60fps) and low memory usage even with massive datasets.

# Skill: CSS Grid vs Flexbox

## Purpose
To choose the right layout module for the task.

## When to Use
- **Flexbox**: 1-Dimensional layout (Row OR Column). Distribution of space within an axis. Alignment.
- **Grid**: 2-Dimensional layout (Rows AND Columns). Precise placement of items on a grid.

## Procedure

### 1. Flexbox (Content-First)
Use for navbars, centering elements, linear lists.
```css
.flex-container {
  display: flex;
  justify-content: space-between; /* Main Axis */
  align-items: center; /* Cross Axis */
  flex-wrap: wrap;
}
```

### 2. CSS Grid (Layout-First)
Use for full page layouts, photo galleries, dashboard cards.
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 equal columns */
  gap: 20px;
}

/* Span items */
.item-1 {
  grid-column: 1 / 3; /* Span 2 cols */
}
```

### 3. Combined
Often used together. Grid for the main page structure, Flexbox for the components inside the grid cells.

## Constraints
- **Complexity**: Grid syntax is more complex (named areas, lines, auto-fill).
- **Subgrid**: `grid-template-columns: subgrid` allows children to align to parent's grid (limited browser support, check CanIUse).

## Expected Output
Robust, responsive layouts using standard CSS without floating or positioning hacks.

# Skill: React Context vs Zustand

## Purpose
To choose and implement the correct state management strategy for React applications to avoid prop-drilling and complexity.

## When to Use
- **Context**: Global constants (Theme, User, Locale) that rarely change.
- **Zustand**: Complex application state (Cart, Dashboard Filters) with frequent updates.

## Procedure

### 1. React Context (Built-in)
Best for dependency injection.
```tsx
const ThemeContext = createContext('light');

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
// Usage: const { theme } = useContext(ThemeContext);
```
**Issue**: When `theme` changes, *all* consumers re-render, even if they only use part of the context.

### 2. Zustand (External Library)
Simple, fast, scalable. Solves the re-render issue via selectors.
```bash
npm install zustand
```

**Store Definition**:
```tsx
import { create } from 'zustand';

const useStore = create((set) => ({
  bears: 0,
  increasePopulation: () => set((state) => ({ bears: state.bears + 1 })),
  removeAllBears: () => set({ bears: 0 }),
}));
```

**Usage**:
```tsx
function BearCounter() {
  const bears = useStore((state) => state.bears); // Selects only 'bears'
  return <h1>{bears} around here ...</h1>;
}
```

## Constraints
- **Boilerplate**: Context requires Providers wrapping the app; Zustand does not.
- **DevTools**: Zustand has Redux DevTools support middleware.

## Expected Output
Optimized rendering performance and cleaner code structure for global state management.

# Skill: Dark Mode Implementation

## Purpose
To provide a color scheme preference (Light/Dark) that respects user system settings and allows manual toggling.

## When to Use
- Improving accessibility and reducing eye strain.
- Modern app aesthetic requirements.

## Procedure

### 1. CSS Variables
Define semantic colors.
```css
:root {
  --bg-primary: #ffffff;
  --text-primary: #000000;
}

[data-theme='dark'] {
  --bg-primary: #1a1a1a;
  --text-primary: #ffffff;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}
```

### 2. Tailwind CSS
Configure `tailwind.config.js`:
```javascript
module.exports = {
  darkMode: 'class', // Use .dark class instead of media query
}
```
Usage: `<div class="bg-white dark:bg-gray-900 text-black dark:text-white">`

### 3. Logic (React Hook)
1.  Check `localStorage` for saved preference.
2.  If none, check system preference: `window.matchMedia('(prefers-color-scheme: dark)').matches`.
3.  Apply class `dark` to `<html>` tag.

```javascript
useEffect(() => {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}, [theme]);
```

## Constraints
- **FOUC**: Flash of Incorrect Theme. Ensure script runs immediately in `<head>` (blocking) to set initial class before body renders.
- **Images**: Invert or dim bright images in dark mode (`filter: brightness(0.8)`).

## Expected Output
Seamless switching between themes with persistence across reloads.

# Skill: Mobile UI Styling (NativeWind)

## Purpose
To style React Native components using the utility-first CSS framework Tailwind CSS, via the **NativeWind** library.

## When to Use
- When you prefer Tailwind syntax over `StyleSheet.create`.
- To share styles/tokens between web and mobile (Universal Apps).
- To speed up UI development with predefined utility classes.

## Procedure

### 1. Installation (NativeWind v4)
1.  Install dependencies:
    ```bash
    npm install nativewind
    npm install --save-dev tailwindcss
    ```
2.  Init Tailwind:
    ```bash
    npx tailwindcss init
    ```

### 2. Configuration
1.  **tailwind.config.js**: Update `content` to include your files.
    ```javascript
    module.exports = {
      content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
      theme: {
        extend: {},
      },
      plugins: [],
    }
    ```
2.  **babel.config.js**: Add the plugin.
    ```javascript
    module.exports = function (api) {
      api.cache(true);
      return {
        presets: ['babel-preset-expo'],
        plugins: ["nativewind/babel"],
      };
    };
    ```

### 3. Usage
Apply classes using the `className` prop (requires setup) or `tw` helper if using older versions.
NativeWind v4 usually supports `className` directly on standard RN components if properly configured with the Babel plugin.

```tsx
import { View, Text } from 'react-native';

export default function Card() {
  return (
    <View className="bg-white p-4 rounded-lg shadow-md">
      <Text className="text-xl font-bold text-gray-800">Hello World</Text>
      <Text className="text-gray-500 mt-2">Styled with NativeWind</Text>
    </View>
  );
}
```

## Constraints
- **Platform Specifics**: Some CSS properties (like `grid`, `z-index` complex behavior) don't map 1:1 to Native.
- **Pseudo-classes**: Hover states don't exist on mobile; focus/active are handled differently.

## Expected Output
Components styled with Tailwind classes that render as native views with optimized performance.

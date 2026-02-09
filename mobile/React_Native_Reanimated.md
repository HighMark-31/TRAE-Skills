# Skill: React Native Reanimated

## Purpose
To create high-performance, smooth (60fps+) animations and interactions in React Native by running animation logic on the UI thread.

## When to Use
- When `Animated` API from React Native is too slow or stutters.
- For complex gestures (drag, pinch, swipe).
- For shared element transitions.

## Procedure

### 1. Setup
1.  **Install**:
    ```bash
    npm install react-native-reanimated
    ```
2.  **Babel Plugin**: Add `react-native-reanimated/plugin` to `babel.config.js` (must be listed **last**).
    ```javascript
    plugins: [
      // other plugins...
      'react-native-reanimated/plugin',
    ],
    ```
3.  **Clear Cache**: `npx expo start -c`.

### 2. Basic Animation (Shared Values)
1.  **Define Value**: Use `useSharedValue`.
    ```tsx
    const width = useSharedValue(100);
    ```
2.  **Define Style**: Use `useAnimatedStyle`.
    ```tsx
    const animatedStyle = useAnimatedStyle(() => {
      return { width: width.value };
    });
    ```
3.  **Render**: Use `Animated.View`.
    ```tsx
    <Animated.View style={[styles.box, animatedStyle]} />
    ```
4.  **Trigger**: Update value with utility functions.
    ```tsx
    width.value = withSpring(200);
    // or withTiming(200, { duration: 500 })
    ```

### 3. Gestures
Combine with `react-native-gesture-handler`.
- Use `GestureDetector` to modify shared values based on touch events.

## Constraints
- **UI Thread Only**: You cannot run complex JS logic inside `useAnimatedStyle` (unless using `runOnJS`).
- **Debugging**: Errors on the UI thread can be harder to trace; use `console.log` carefully or `runOnJS` for debugging.

## Expected Output
Fluid animations that do not block the Javascript thread, providing a "native" feel.

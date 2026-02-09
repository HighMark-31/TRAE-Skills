# Skill: React Native Navigation

## Purpose
To implement robust navigation patterns in React Native applications using **Expo Router** (recommended) or **React Navigation**.

## When to Use
- When the app has multiple screens.
- When needing tab bars, drawers, or stack navigation (push/pop).
- When handling deep links.

## Procedure

### Option A: Expo Router (File-based, Modern)
1.  **Setup**: Ensure `expo-router` is installed.
    ```bash
    npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-constants
    ```
2.  **Structure**:
    - `app/index.tsx`: The home screen.
    - `app/_layout.tsx`: Defines the layout (Stack/Tabs).
    - `app/details/[id].tsx`: Dynamic route.
3.  **Implementation**:
    - Use `<Stack />` or `<Tabs />` in `_layout.tsx`.
    - Navigate using `<Link href="/details/1">` or `router.push('/details/1')`.

### Option B: React Navigation (Component-based, Traditional)
1.  **Install**:
    ```bash
    npm install @react_navigation/native @react_navigation/native-stack
    npx expo install react-native-screens react-native-safe-area-context
    ```
2.  **Implementation**:
    ```tsx
    import { NavigationContainer } from '@react_navigation/native';
    import { createNativeStackNavigator } from '@react_navigation/native-stack';

    const Stack = createNativeStackNavigator();

    export default function App() {
      return (
        <NavigationContainer>
          <Stack.Navigator>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Details" component={DetailsScreen} />
          </Stack.Navigator>
        </NavigationContainer>
      );
    }
    ```

## Constraints
- **Type Safety**: Always type routes for `useNavigation` and `useRoute` hooks to avoid runtime errors.
- **Nesting**: Avoid deep nesting of navigators to prevent performance issues and state complexity.

## Expected Output
A navigation structure allowing smooth transitions between screens, preserving history and state.

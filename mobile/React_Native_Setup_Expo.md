# Skill: React Native Setup (Expo)

## Purpose
To initialize a scalable, cross-platform mobile application using React Native and Expo, configured with TypeScript and standard linting tools.

## When to Use
- Starting a new mobile project for iOS and Android.
- Prototyping rapidly without complex native build setups.
- When needing access to native device features via a managed workflow.

## Procedure

### 1. Prerequisites
- Node.js (LTS) installed.
- Git installed.
- Expo CLI (optional globally, better via npx).
- Expo Go app on physical device (iOS/Android).

### 2. Initialization
Run the create command with the default TypeScript template:
```bash
npx create-expo-app@latest my-app --template default
```

### 3. Configuration
1.  **TypeScript**: Ensure `tsconfig.json` is present. If not, create an empty one and run `npx expo start` to auto-generate it.
2.  **Linting**:
    ```bash
    npm install --save-dev eslint @react-native-community/eslint-config prettier
    ```
    Create `.eslintrc.js`:
    ```javascript
    module.exports = {
      root: true,
      extends: '@react-native-community',
    };
    ```
3.  **Project Structure**:
    - `app/`: For Expo Router (if using file-based routing).
    - `components/`: Reusable UI components.
    - `assets/`: Images and fonts.
    - `constants/`: Theme colors and global config.

### 4. Running the Project
1.  Start the development server:
    ```bash
    npx expo start
    ```
2.  **Physical Device**: Scan the QR code with Expo Go.
3.  **Simulator**: Press `i` for iOS Simulator or `a` for Android Emulator (requires Xcode/Android Studio).

## Constraints
- **Native Modules**: If a library requires native code linking not supported by Expo Go, use "Development Builds" (`npx expo run:ios`).
- **File Size**: Keep assets optimized to reduce bundle size.

## Expected Output
A running React Native application on a simulator or device, with hot reloading enabled and TypeScript configured.

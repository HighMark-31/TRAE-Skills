# Skill: Mobile Device Features

## Purpose
To access native device hardware capabilities (Camera, Location, Sensors, Biometrics) securely and efficiently in Expo/React Native.

## When to Use
- When the app needs to take photos, track user location, or use FaceID.
- When reading accelerometer or gyroscope data.

## Procedure

### 1. Permissions (Crucial)
Always request permission before accessing features.
- **Android**: Permissions are added to `app.json` (Expo) or `AndroidManifest.xml`.
- **iOS**: Info.plist keys are added to `app.json`.

### 2. Implementation: Camera (Example)
1.  **Install**: `npx expo install expo-camera`
2.  **Usage**:
    ```tsx
    import { CameraView, useCameraPermissions } from 'expo-camera';

    export default function App() {
      const [permission, requestPermission] = useCameraPermissions();

      if (!permission) return <View />;
      if (!permission.granted) {
        return <Button onPress={requestPermission} title="Grant Permission" />;
      }

      return (
        <CameraView style={{ flex: 1 }} facing="back">
          {/* Camera UI */}
        </CameraView>
      );
    }
    ```

### 3. Implementation: Location
1.  **Install**: `npx expo install expo-location`
2.  **Usage**:
    ```tsx
    import * as Location from 'expo-location';

    // inside component
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') return;

    const location = await Location.getCurrentPositionAsync({});
    ```

## Constraints
- **Privacy**: Only request permissions when necessary. Explain *why* to the user.
- **Simulator**: Some features (Camera, Gyroscope) may not work on Simulators; test on real devices.
- **Background Usage**: Requires special permissions and configuration (Background Tasks).

## Expected Output
Functional integration with device hardware, handling permission flows gracefully (granted, denied, restricted).

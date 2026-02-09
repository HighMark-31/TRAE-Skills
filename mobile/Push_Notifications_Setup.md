# Skill: Push Notifications Setup

## Purpose
To implement remote push notifications to engage users, using Expo Notifications service (FCM for Android, APNs for iOS).

## When to Use
- To inform users of updates, messages, or alerts.
- To re-engage users who haven't opened the app recently.

## Procedure

### 1. Configuration (Expo)
1.  **Install**: `npx expo install expo-notifications expo-device expo-constants`.
2.  **App.json**: Configure `extra.eas.projectId`.

### 2. Permission & Token Retrieval
Create a hook to get the Expo Push Token:
```tsx
async function registerForPushNotificationsAsync() {
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'default',
      importance: Notifications.AndroidImportance.MAX,
    });
  }

  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return;

  const token = (await Notifications.getExpoPushTokenAsync()).data;
  return token; // Send this to your backend
}
```

### 3. Handling Notifications
1.  **Foreground**:
    ```tsx
    Notifications.setNotificationHandler({
      handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: false,
      }),
    });
    ```
2.  **Background/Interaction**: Add listeners:
    - `addNotificationReceivedListener`: Triggered when received.
    - `addNotificationResponseReceivedListener`: Triggered when user taps the notification.

### 4. Sending (Backend)
Send requests to `https://exp.host/--/api/v2/push/send`.
```json
{
  "to": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]",
  "title": "hello",
  "body": "world"
}
```

## Constraints
- **Credentials**: You must upload APNs Key (iOS) and FCM Server Key (Android) to Expo dashboard/EAS.
- **Testing**: Push notifications generally do NOT work on Simulators; use a physical device.

## Expected Output
A system where the device receives a token, sends it to the server, and the server can trigger a notification appearing on the device.

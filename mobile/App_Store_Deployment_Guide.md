# Skill: App Store Deployment Guide

## Purpose
To prepare, build, and submit React Native applications to the Apple App Store and Google Play Store using **EAS Build** (Expo Application Services).

## When to Use
- When the app is ready for beta testing (TestFlight/Internal Testing) or production release.
- When generating standalone binaries (.ipa, .aab).

## Procedure

### 1. Configuration (EAS)
1.  **Install EAS CLI**: `npm install -g eas-cli`.
2.  **Login**: `eas login`.
3.  **Configure**: `eas build:configure`. This creates `eas.json`.

### 2. App Signing (Credentials)
- **Android**: Need a Keystore. EAS can generate and manage this automatically.
- **iOS**: Need an Apple Developer Account ($99/yr). EAS manages Certificates and Provisioning Profiles.

### 3. Building
1.  **Update Version**: Check `version` and `android.versionCode` / `ios.buildNumber` in `app.json`.
2.  **Run Build**:
    ```bash
    eas build --platform all --profile production
    ```
    - This uploads code to Expo servers, builds the binary, and returns a download link.

### 4. Submission (EAS Submit)
Automate the upload to stores.
1.  **Run Submit**:
    ```bash
    eas submit --platform all
    ```
2.  **Follow Prompts**: Select the build to submit.

### 5. Store Metadata
- Go to App Store Connect / Google Play Console.
- Fill in descriptions, screenshots, privacy policy, and rating questionnaire.
- Select the build uploaded by EAS and submit for review.

## Constraints
- **Review Guidelines**: Ensure the app complies with Apple/Google policies (e.g., no hidden features, functional UI).
- **Waiting Times**: Apple review takes 24-48h; Google takes 1-3 days (sometimes longer for new accounts).

## Expected Output
A successful build uploaded to TestFlight (iOS) and Internal Testing (Android), ready for distribution.

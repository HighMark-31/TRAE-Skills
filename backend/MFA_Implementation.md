# Skill: MFA Implementation

## Purpose
To add an extra layer of security (Multi-Factor Authentication) using Time-based One-Time Passwords (TOTP).

## When to Use
- Protecting sensitive accounts (Admin panels, financial apps).
- Compliance requirements.

## Procedure

### 1. Setup
Use `otplib` and `qrcode`.
```bash
npm install otplib qrcode
```

### 2. Registration (Enable MFA)
1.  **Generate Secret**:
    ```javascript
    const secret = authenticator.generateSecret(); // Store this encrypted in DB!
    ```
2.  **Generate QR Code**:
    ```javascript
    const otpauth = authenticator.keyuri('user@example.com', 'MyApp', secret);
    const imageUrl = await qrcode.toDataURL(otpauth);
    // Send imageUrl to frontend for user to scan with Google Authenticator
    ```
3.  **Verify Setup**: Ask user to enter the code they see to confirm setup.

### 3. Login Verification
1.  User enters username/password.
2.  Check if MFA is enabled. If yes, return intermediate state.
3.  User enters TOTP code.
4.  **Verify**:
    ```javascript
    const isValid = authenticator.verify({ token: userToken, secret: userSecret });
    if (!isValid) throw new Error('Invalid code');
    ```
5.  Issue Session/JWT.

### 4. Recovery Codes
Always generate a set of one-time use recovery codes (e.g., 10 codes) when enabling MFA, in case the user loses their device. Store these hashed in the DB.

## Constraints
- **Time Drift**: TOTP relies on server and client time being synced. `otplib` handles a default window (+- 30s).
- **Security**: Never send the secret to the client after the initial QR code generation.

## Expected Output
A secure authentication flow requiring "something you know" (password) and "something you have" (TOTP device).

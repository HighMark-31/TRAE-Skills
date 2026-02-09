# Skill: OAuth2 Provider Implementation

## Purpose
To secure an API by implementing an OAuth2 authorization server, allowing third-party clients to access resources on behalf of a user.

## When to Use
- When building a platform where other developers build apps (like "Login with Google").
- When separating Authentication (Identity) from Authorization (Access).

## Procedure

### 1. Terminology
- **Resource Owner**: The User.
- **Client**: The 3rd party app.
- **Authorization Server**: Issues tokens.
- **Resource Server**: The API hosting data.

### 2. Grant Types
Choose the right flow:
- **Authorization Code**: For server-side apps (Most common, secure).
- **PKCE**: Extension of Auth Code for mobile/SPA (Mandatory for public clients).
- **Client Credentials**: Machine-to-machine communication.

### 3. Implementation Steps (Node.js example using `oauth2-server`)
1.  **Define Model**: Implement `getClient`, `saveToken`, `getAccessToken`, `verifyScope`.
    ```javascript
    // model.js
    module.exports = {
      getClient: async (clientId, clientSecret) => { ... },
      saveToken: async (token, client, user) => { ... },
      getAccessToken: async (accessToken) => { ... },
      // ...
    };
    ```
2.  **Initialize Server**:
    ```javascript
    const OAuth2Server = require('oauth2-server');
    const oauth = new OAuth2Server({
      model: require('./model'),
      accessTokenLifetime: 3600,
      allowBearerTokensInQueryString: true
    });
    ```
3.  **Endpoints**:
    - `POST /oauth/token`: Exchange code for token.
    - `POST /oauth/authorize`: User approves access (renders login/consent page).
4.  **Middleware**: Protect API routes.
    ```javascript
    app.get('/secure', authenticateRequest, (req, res) => {
      res.json({ data: 'secret' });
    });
    ```

## Constraints
- **Security**: Never implement OAuth2 from scratch crypto logic. Use established libraries (`node-oauth2-server`, `panva/node-oidc-provider`).
- **HTTPS**: OAuth2 requires TLS/SSL in production to protect tokens.

## Expected Output
A compliant OAuth2 interface issuing Access Tokens and Refresh Tokens, enabling secure delegated access.

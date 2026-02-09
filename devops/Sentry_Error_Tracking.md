# Skill: Sentry Error Tracking Setup

## Purpose
To track application errors.

## When to Use
- SDK setup and source maps.
- When the specific requirement for Sentry Error Tracking Setup arises in the project.

## Procedure

### 1. SDK Installation
Install the Sentry SDK for your platform.

```bash
# For Node.js
npm install @sentry/node @sentry/profiling-node
```

### 2. Initialization
Initialize Sentry as early as possible in your application.

```javascript
import * as Sentry from "@sentry/node";
import { nodeProfilingIntegration } from "@sentry/profiling-node";

Sentry.init({
  dsn: "https://your-public-key@sentry.io/project-id",
  integrations: [
    nodeProfilingIntegration(),
  ],
  // Performance Monitoring
  tracesSampleRate: 1.0, // Capture 100% of transactions in dev
  // Set sampling rate for profiling - this is relative to tracesSampleRate
  profilesSampleRate: 1.0,
});
```

### 3. Capturing Errors
Sentry automatically captures unhandled exceptions, but you can also capture errors manually.

```javascript
try {
  doSomethingRisky();
} catch (e) {
  Sentry.captureException(e, {
    extra: { context: "risky_operation" },
    tags: { feature: "billing" }
  });
}
```

### 4. Integrating with Express
Add Sentry handlers to your Express app for automatic request tracking.

```javascript
const app = express();

// The request handler must be the first middleware on the app
app.use(Sentry.Handlers.requestHandler());

// ... your routes ...

// The error handler must be before any other error middleware and after all controllers
app.use(Sentry.Handlers.errorHandler());
```

## Constraints
- **PII Protection**: Use `beforeSend` or Sentry's data scrubbing features to remove sensitive user data (passwords, tokens) from reports.
- **Source Maps**: Upload source maps to Sentry during your build process to see original code in stack traces instead of minified code.
- **Sampling**: In high-traffic production environments, lower the `tracesSampleRate` (e.g., 0.1 or 0.01) to avoid performance impact and cost.

## Expected Output
Real-time error notifications with full stack traces, breadcrumbs (user actions leading to the error), and environment details in the Sentry dashboard.

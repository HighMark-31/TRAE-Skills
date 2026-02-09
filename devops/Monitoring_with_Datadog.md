# Skill: Monitoring with Datadog

## Purpose
To observe system health.

## When to Use
- Metrics, dashboards, and alerts.
- When the specific requirement for Monitoring with Datadog arises in the project.

## Procedure

### 1. Agent Installation
Deploy the Datadog Agent to your infrastructure (using Docker/Kubernetes).

```yaml
# datadog-agent.yaml (K8s)
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
spec:
  template:
    spec:
      containers:
        - name: datadog-agent
          image: gcr.io/datadoghq/agent:latest
          env:
            - name: DD_API_KEY
              valueFrom:
                secretKeyRef:
                  name: datadog-secret
                  key: api-key
```

### 2. Application Instrumentation (Node.js)
Install the `dd-trace` library and initialize it at the very top of your entry file.

```javascript
// index.js - MUST BE THE FIRST LINE
require('dd-trace').init({
  env: 'production',
  service: 'my-backend-service',
  version: '1.0.0',
  logInjection: true // Links logs to traces
});

const express = require('express');
const app = express();
// ... rest of your app
```

### 3. Custom Metrics and Tags
Send custom business metrics to Datadog.

```javascript
const stats = require('hot-shots');
const dogstatsd = new stats();

// Increment a counter with tags
dogstatsd.increment('checkout.completed', 1, ['plan:pro', 'region:us-east']);

// Gauge for current status
dogstatsd.gauge('active.sessions', 150);
```

### 4. Setting up Monitors (Alerts)
Create monitors via the UI or Terraform to alert on specific thresholds.
- **Metric Monitor**: Alert if `avg(last_5m):avg:system.cpu.user{host:my-app} > 80`.
- **Anomaly Detection**: Alert if request latency deviates from seasonal patterns.

## Constraints
- **Sampling**: Adjust sampling rates for high-traffic apps to control costs.
- **Tagging**: Use consistent tags (`env`, `service`, `team`) for efficient filtering.
- **Security**: Mask PII (Personally Identifiable Information) in logs and traces using Datadog's sensitive data scanner.

## Expected Output
A fully instrumented application providing real-time dashboards, traces, and automated alerts in the Datadog platform.

# Skill: Monitoring & Alerting (Prometheus/Grafana)

## Purpose
To collect metrics (CPU, Memory, Request Latency, Error Rates) and alert engineers when the system behaves abnormally.

## When to Use
- Production readiness.
- Capacity planning.
- Detecting incidents before users report them.

## Procedure

### 1. Application Instrumentation (Node.js)
Install `prom-client` and expose the `/metrics` endpoint.

```javascript
const express = require('express');
const client = require('prom-client');

const app = express();
const register = new client.Registry();

// Add default metrics (CPU, Memory, etc.)
client.collectDefaultMetrics({ register });

// Define a custom metric
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.5, 1, 2, 5]
});
register.registerMetric(httpRequestDuration);

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

### 2. Prometheus Configuration
Configure Prometheus to scrape your application in `prometheus.yml`.

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'my-backend-service'
    static_configs:
      - targets: ['myapp:3000']
    metrics_path: '/metrics'
```

### 3. Alerting Rules
Define rules for Alertmanager to trigger notifications.

```yaml
# alert_rules.yml
groups:
- name: APIAlerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status_code=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "High Error Rate on {{ $labels.instance }}"
      description: "Error rate is above 5% for more than 2 minutes."
```

### 4. Grafana Dashboard Setup
1. Add Prometheus as a Data Source.
2. Import common dashboards (e.g., ID: 1860 for Node.js Exporter).
3. Create custom panels using PromQL:
   - **Throughput**: `sum(rate(http_requests_total[1m])) by (method)`
   - **P95 Latency**: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`

## Constraints
- **Cardinality**: Never use high-cardinality values (like User IDs, UUIDs, or email addresses) as Prometheus labels. This will cause memory usage to explode.
- **Actionable Alerts**: Only alert on symptoms that affect users (e.g., high error rate, high latency) rather than causes (e.g., high CPU) unless they are predictive of failure.
- **Scrape Interval**: Ensure the `scrape_interval` is consistent with your alerting `for` duration to avoid false positives.

## Expected Output
A monitoring dashboard and an active alerting pipeline for critical system health indicators.

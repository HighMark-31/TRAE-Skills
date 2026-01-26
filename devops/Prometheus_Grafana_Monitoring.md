# Skill: Monitoring & Alerting (Prometheus/Grafana)

## Purpose
To collect metrics (CPU, Memory, Request Latency, Error Rates) and alert engineers when the system behaves abnormally.

## When to Use
- Production readiness.
- Capacity planning.
- Detecting incidents before users report them.

## Procedure
1.  **Expose Metrics**: Add an endpoint `/metrics` to the app (using `prom-client` for Node.js).
2.  **Scrape**: Configure Prometheus to scrape the application targets at intervals (e.g., 15s).
3.  **Visualize**: Connect Grafana to Prometheus and build dashboards (Golden Signals: Latency, Traffic, Errors, Saturation).
4.  **Alerting**:
    - Define rules in Prometheus (e.g., `rate(http_requests_total{status=~"5.."}[5m]) > 1`).
    - Configure Alertmanager to send notifications to Slack/PagerDuty.

## Constraints
- High cardinality labels (e.g., `user_id`) can crash Prometheus; avoid them.
- Alerts should be actionable (don't alert on "CPU high" unless it impacts performance; alert on "Error Rate High").

## Expected Output
A monitoring dashboard and an active alerting pipeline for critical system health indicators.

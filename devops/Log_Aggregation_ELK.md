# Skill: Log Aggregation (ELK/Loki)

## Purpose
To centralize logs from all services and containers into a single queryable interface, enabling debugging and trend analysis across the distributed system.

## When to Use
- When running multiple microservices or containers.
- When SSH-ing into servers to check logs is not scalable.

## Procedure

### 1. Application Logging (Node.js with Winston)
Configure your application to output structured logs (JSON) to standard output.

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json() // Essential for log aggregators to parse easily
  ),
  defaultMeta: { service: 'user-service' },
  transports: [
    new winston.transports.Console(),
  ],
});

// Example log
logger.info('User logged in', { userId: '123', ip: '192.168.1.1' });
```

### 2. Log Collection (Filebeat for ELK)
Configure Filebeat to harvest logs from Docker containers.

```yaml
# filebeat.yml
filebeat.inputs:
- type: container
  paths:
    - /var/lib/docker/containers/*/*.log

processors:
- add_docker_metadata: ~
- decode_json_fields:
    fields: ["message"]
    target: "json"
    overwrite_keys: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"
```

### 3. Log Shipping (Promtail for Loki)
If using the PLG stack, configure Promtail as a DaemonSet.

```yaml
# promtail-config.yaml
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
- job_name: kubernetes-pods
  kubernetes_sd_configs:
    - role: pod
  relabel_configs:
    - source_labels: [__meta_kubernetes_pod_label_app]
      target_label: app
```

### 4. Querying and Visualization
- **Kibana (ELK)**: Use KQL (Kibana Query Language) to search logs.
  - `json.userId: "123" AND level: "error"`
- **Grafana (Loki)**: Use LogQL to filter and aggregate.
  - `{app="user-service"} |= "error" | json`

## Constraints
- **Structured Logging**: Always log in JSON format. Parsing unstructured text logs with regex is brittle and CPU-intensive for the aggregator.
- **Log Rotation**: Ensure the host system rotates local log files (e.g., via Docker's `max-size` and `max-file` options) to prevent disk exhaustion.
- **PII Redaction**: Never log sensitive information like passwords, credit card numbers, or full PII. Implement redaction in the logging library or the shipping agent.
- **Volume Management**: Use sampling or level filtering (e.g., only `warn` and `error` in production) if log volume becomes too expensive.

## Expected Output
A logging pipeline where application logs appear in the visualization tool within seconds of generation.

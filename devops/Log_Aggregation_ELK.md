# Skill: Log Aggregation (ELK/Loki)

## Purpose
To centralize logs from all services and containers into a single queryable interface, enabling debugging and trend analysis across the distributed system.

## When to Use
- When running multiple microservices or containers.
- When SSH-ing into servers to check logs is not scalable.

## Procedure
1.  **Choose Stack**: ELK (Elasticsearch, Logstash, Kibana) or PLG (Promtail, Loki, Grafana).
2.  **Instrument Application**: Ensure app logs to STDOUT/STDERR in JSON format (using Winston/Bunyan).
3.  **Ship Logs**:
    - **Docker**: Configure Docker daemon to use `json-file` driver or send directly to Fluentd.
    - **Agent**: Run a log collector (Filebeat/Promtail) as a DaemonSet on K8s nodes.
4.  **Index/Store**: The collector pushes logs to the storage engine (Elasticsearch/Loki).
5.  **Visualize**: Create dashboards in Kibana/Grafana to filter by `service_name`, `level`, or `trace_id`.

## Constraints
- Rotate logs on disk to prevent filling up storage before shipping.
- Filter out sensitive data (PII) before shipping.
- monitor the log volume to manage costs.

## Expected Output
A logging pipeline where application logs appear in the visualization tool within seconds of generation.

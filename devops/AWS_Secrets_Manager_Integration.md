# Skill: AWS Secrets Manager Integration

## Purpose
To retrieve secrets (database credentials, API keys) at runtime rather than storing them in environment variables or config files, enabling automatic rotation and better security.

## When to Use
- High-security environments.
- When key rotation is required by compliance.

## Procedure
1.  **Store Secret**: Create a secret in AWS Secrets Manager (JSON key/value).
2.  **IAM Role**: Grant the application's IAM Role permission to `secretsmanager:GetSecretValue`.
3.  **Application Code**:
    - Use AWS SDK (`@aws-sdk/client-secrets-manager`).
    - On startup, fetch the secret by ID.
    - Parse JSON and set config values.
4.  **Caching**: Cache the secret in memory for a short duration to avoid hitting API limits and latency costs.
5.  **Rotation**: (Advanced) Configure Lambda to rotate the secret (e.g., change DB password) automatically.

## Constraints
- Handle network failures when fetching secrets.
- Do not log the retrieved secrets.
- Fallback strategy (if service is down) - usually fail hard for security.

## Expected Output
An application that boots up by fetching its configuration securely from a managed vault service.

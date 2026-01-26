# Skill: Health Check Endpoint Implementation

## Purpose
To provide a standard endpoint that load balancers and orchestration systems (Kubernetes, AWS Target Groups) use to verify the application is running and ready to accept traffic.

## When to Use
- When deploying to a container orchestration platform.
- When setting up a load balancer.
- When implementing uptime monitoring.

## Procedure
1.  **Define Liveness Probe**:
    - Route: `/health/live` (or just `/health`).
    - Logic: Return 200 OK immediately if the process is up.
2.  **Define Readiness Probe**:
    - Route: `/health/ready`.
    - Logic: Check connections to critical dependencies (Database, Redis).
    - If connected: Return 200 OK.
    - If disconnected: Return 503 Service Unavailable.
3.  **Security**:
    - Ensure these endpoints are lightweight and do not expose sensitive system info.
    - Optionally protect detailed info behind internal IP whitelists.
4.  **Response Format**:
    - JSON: `{ status: "ok", timestamp: "...", services: { db: "up", redis: "up" } }`.

## Constraints
- Liveness check must be extremely fast and simple.
- Readiness check must not be too heavy (cache results if necessary) to avoid dDoSing the database during checks.

## Expected Output
One or two API endpoints enabling automated systems to monitor application health and traffic readiness.

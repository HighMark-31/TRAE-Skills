# Skill: Kubernetes Deployment Manifests

## Purpose
To define how applications should run, scale, and update within a Kubernetes cluster using declarative YAML manifests.

## When to Use
- Deploying containerized applications to K8s.
- Defining resource limits, replicas, and environment variables.

## Procedure
1.  **Define Deployment**: Create `deployment.yaml`.
    - Set `replicas` (e.g., 3).
    - Define `containers` (image, ports, env).
    - Add `livenessProbe` and `readinessProbe`.
    - Set `resources` (requests/limits) to prevent starvation.
2.  **Define Service**: Create `service.yaml` to expose pods (ClusterIP, NodePort, or LoadBalancer).
3.  **Define ConfigMap/Secret**: Extract config and secrets from the deployment YAML.
4.  **Apply**: Run `kubectl apply -f ./k8s/`.
5.  **Verify**: `kubectl get pods`, `kubectl describe deployment <name>`.

## Constraints
- Do not use `latest` tag for images; use specific versions or SHA.
- Always set CPU/Memory limits.
- Use Namespaces to isolate environments (`dev`, `staging`, `prod`).

## Expected Output
Valid YAML files (`deployment.yaml`, `service.yaml`) that successfully launch the application in a cluster.

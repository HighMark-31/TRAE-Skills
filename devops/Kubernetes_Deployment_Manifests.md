# Skill: Kubernetes Deployment Manifests

## Purpose
To define how applications should run, scale, and update within a Kubernetes cluster using declarative YAML manifests.

## When to Use
- Deploying containerized applications to K8s.
- Defining resource limits, replicas, and environment variables.

## Procedure

### 1. Deployment Manifest
Create a `deployment.yaml` to manage your application's lifecycle.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-registry/my-app:1.2.3
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: my-app-config
        - secretRef:
            name: my-app-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
```

### 2. Service Manifest
Create a `service.yaml` to expose the application within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP # Internal exposure only
```

### 3. ConfigMap and Secrets
Decouple configuration from the deployment.

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-app-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"

---
# secret.yaml (values must be base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: my-app-secrets
type: Opaque
data:
  DATABASE_URL: bXktZGItaG9zdC1jb25uZWN0aW9uLXN0cmluZw==
```

### 4. Applying and Managing
Use `kubectl` to apply the manifests and check status.

```bash
# Apply all files in the directory
kubectl apply -f ./k8s/

# Check rollout status
kubectl rollout status deployment/my-app-deployment

# Get logs from a specific pod
kubectl logs -l app=my-app --tail=100

# Scale the deployment
kubectl scale deployment/my-app-deployment --replicas=5
```

## Constraints
- **Immutable Tags**: Do not use the `latest` tag; use specific versions or image SHAs to ensure reproducibility.
- **Resource Limits**: Always set CPU and Memory requests and limits to prevent a single container from crashing the node.
- **Probes**: Implement both `liveness` (restart if hung) and `readiness` (don't send traffic until ready) probes.
- **Secrets Management**: Do not commit raw `secret.yaml` files to Git. Use tools like Sealed Secrets, External Secrets, or HashiCorp Vault.

## Expected Output
Valid YAML files (`deployment.yaml`, `service.yaml`) that successfully launch the application in a cluster.

# Skill: Microservice Communication (gRPC/HTTP)

## Purpose
To enable reliable and efficient communication between distinct services in a distributed architecture.

## When to Use
- Breaking a monolith into services.
- Connecting a backend to a specialized service (e.g., AI inference, Payment Gateway).

## Procedure
1.  **Choose Protocol**:
    - **HTTP/REST**: Simple, ubiquitous, text-based (JSON). Good for public or loose coupling.
    - **gRPC (Protobuf)**: Binary, strongly typed, high performance. Good for internal service-to-service.
2.  **Define Contract**:
    - REST: OpenAPI spec.
    - gRPC: `.proto` file defining messages and services.
3.  **Implement Client**: Create a client wrapper to make requests (handle retries, timeouts).
4.  **Implement Server**: Implement the handler for the request.
5.  **Service Discovery**: Mechanism to find the target service IP/Port (DNS, Consul, K8s Services).

## Constraints
- Handle network failures (timeouts, retries with exponential backoff).
- Implement Circuit Breaker pattern to prevent cascading failures.
- Ensure backward compatibility when changing contracts.

## Expected Output
A client-server setup allowing two distinct applications to exchange data efficiently and reliably.

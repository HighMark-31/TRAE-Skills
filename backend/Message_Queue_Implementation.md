# Skill: Message Queue Implementation (RabbitMQ/SQS)

## Purpose
To decouple heavy or long-running processes from the main HTTP request-response cycle by offloading tasks to an asynchronous background worker.

## When to Use
- When sending emails/notifications.
- When processing video/image uploads.
- When handling high-throughput event ingestion.

## Procedure
1.  **Setup Producer**:
    - Connect to the message broker (e.g., `amqplib` for RabbitMQ).
    - Serialize the task payload (JSON).
    - Publish the message to a specific queue or exchange.
2.  **Setup Consumer (Worker)**:
    - Run a separate process or service.
    - Subscribe to the queue.
    - Process messages one by one (or in batches).
3.  **Ack/Nack Strategy**:
    - If processing succeeds, acknowledge (`ack`) the message to remove it.
    - If it fails, negative acknowledge (`nack`) to requeue or send to Dead Letter Queue (DLQ).
4.  **Dead Letter Queue**: Configure a DLQ for messages that fail repeatedly to prevent infinite loops.

## Constraints
- Messages must be idempotent (processing the same message twice shouldn't break things).
- Ensure the message payload size is within limits.
- Handle connection drops and retries gracefully.

## Expected Output
A producer module for sending messages and a worker script for consuming and processing them reliably.

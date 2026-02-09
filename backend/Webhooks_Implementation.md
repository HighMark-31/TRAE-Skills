# Skill: Webhooks Implementation

## Purpose
To implement a system that pushes real-time event notifications to external subscribers via HTTP POST requests.

## When to Use
- Notifying 3rd party integrations of state changes (e.g., "Payment Successful", "Order Shipped").
- Reducing polling from clients.

## Procedure

### 1. Subscription Management
Create a database table to store subscriber URLs and the events they are interested in.
- `id`, `user_id`, `target_url`, `event_types` (array), `secret_key` (for signing).

### 2. Event Triggering
When an event occurs in the system:
1.  Construct the payload: `{ id: "evt_123", type: "order.created", data: { ... } }`.
2.  Find active subscriptions for this event type.
3.  Enqueue a background job (using BullMQ/RabbitMQ) to send the webhook. **Do not send synchronously** to avoid blocking the request.

### 3. Delivery (The Worker)
1.  **Signature**: Generate an HMAC signature of the payload using the subscriber's secret key.
    ```javascript
    const signature = crypto.createHmac('sha256', secret).update(JSON.stringify(payload)).digest('hex');
    ```
2.  **Request**: Send POST request with signature header (e.g., `X-Signature`).
3.  **Retry Logic**: Implement exponential backoff if the subscriber returns 5xx or times out. Disable subscription after N consecutive failures.

### 4. Security
- **Signing**: Allows receivers to verify the request came from you.
- **Timeouts**: Set short timeouts (e.g., 5s) to prevent stuck workers.
- **SSRF Prevention**: Validate `target_url` to ensure it doesn't point to internal network addresses (localhost, 192.168.x.x).

## Constraints
- **Ordering**: Delivery order is not guaranteed in distributed systems. Include a timestamp in the payload.
- **Idempotency**: Receivers should handle duplicate webhooks gracefully (using event ID).

## Expected Output
A robust event delivery system allowing external systems to react to internal changes in near real-time.

# Skill: Distributed Transactions (Sagas)

## Purpose
To maintain data consistency across multiple microservices where local ACID transactions are not possible.

## When to Use
- E-commerce order: Payment Service -> Inventory Service -> Shipping Service.
- Any operation spanning multiple databases.

## Procedure

### 1. The Saga Pattern
A sequence of local transactions. If one fails, execute **Compensating Transactions** to undo changes.

### 2. Choreography (Event-Based)
Services listen to events and trigger the next step.
1.  **Order Service**: Creates Order (Pending). Publishes `OrderCreated`.
2.  **Payment Service**: Listens to `OrderCreated`. Charges card. Publishes `PaymentProcessed` or `PaymentFailed`.
3.  **Inventory Service**: Listens to `PaymentProcessed`. Reserves stock. Publishes `StockReserved`.
4.  **Order Service**: Listens to `StockReserved`. Updates Order to `Confirmed`.

**Compensation**:
- If Payment fails: Publish `PaymentFailed`.
- Order Service listens: Cancels Order.

### 3. Orchestration (Controller-Based)
A central "Saga Orchestrator" tells services what to do.
1.  **Orchestrator**: Send "Reserve Stock" command to Inventory.
2.  **Inventory**: Responds "Success".
3.  **Orchestrator**: Send "Charge Payment" command.
4.  **Payment**: Responds "Insufficient Funds".
5.  **Orchestrator**: Send "Release Stock" command (Compensation) to Inventory.

### 4. Implementation
Use frameworks like Temporal.io or custom state machines with message queues (BullMQ/Kafka).

## Constraints
- **Eventual Consistency**: The system is not consistent at every moment. UI must handle "Pending" states.
- **Isolation**: Sagas lack Isolation (I in ACID). "Dirty reads" can happen. Use semantic locking (e.g., state=PENDING_APPROVAL) to prevent other ops from touching the entity.

## Expected Output
A resilient distributed workflow that guarantees the system eventually reaches a consistent state (either Success or Rolled Back).

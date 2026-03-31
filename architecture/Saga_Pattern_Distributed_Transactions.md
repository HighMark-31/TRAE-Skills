# Skill: Saga Pattern for Distributed Transactions

## Purpose
To manage data consistency across multiple microservices without using two-phase commit, using a sequence of local transactions coordinated through events.

## When to Use
- When implementing distributed transactions across microservices
- When you need eventual consistency rather than immediate consistency
- When long-running transactions span multiple services
- When you need compensating transactions for rollback

## Procedure

### 1. Saga Pattern Foundation
Implement the basic saga pattern structure.

```python
from abc import ABC, abstractmethod
from typing import List, Any, Dict
import logging
from enum import Enum

class SagaStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"

class SagaStep(ABC):
    """Abstract base class for saga steps."""
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the step."""
        pass
    
    @abstractmethod
    async def compensate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Compensate the step."""
        pass

class Saga:
    """Saga orchestrator for distributed transactions."""
    
    def __init__(self, name: str, steps: List[SagaStep]):
        self.name = name
        self.steps = steps
        self.status = SagaStatus.PENDING
        self.current_step = 0
        self.context = {}
        self.logger = logging.getLogger(f"Saga.{name}")
    
    async def execute(self, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the saga."""
        self.context = initial_context or {}
        self.status = SagaStatus.RUNNING
        self.logger.info(f"Starting saga: {self.name}")
        
        try:
            # Execute each step
            for i, step in enumerate(self.steps):
                self.current_step = i
                self.logger.info(f"Executing step {i + 1}/{len(self.steps)}: {step.__class__.__name__}")
                
                step_result = await step.execute(self.context)
                self.context.update(step_result)
            
            # All steps completed successfully
            self.status = SagaStatus.COMPLETED
            self.logger.info(f"Saga completed successfully: {self.name}")
            
            return self.context
            
        except Exception as e:
            self.logger.error(f"Saga failed at step {self.current_step}: {str(e)}")
            self.status = SagaStatus.FAILED
            
            # Start compensation
            await self._compensate()
            
            raise
    
    async def _compensate(self):
        """Compensate completed steps."""
        self.status = SagaStatus.COMPENSATING
        self.logger.info(f"Starting compensation for saga: {self.name}")
        
        # Compensate in reverse order
        for i in range(self.current_step - 1, -1, -1):
            step = self.steps[i]
            self.logger.info(f"Compensating step {i + 1}: {step.__class__.__name__}")
            
            try:
                compensate_result = await step.compensate(self.context)
                self.context.update(compensate_result)
            except Exception as e:
                self.logger.error(f"Compensation failed at step {i}: {str(e)}")
        
        self.status = SagaStatus.COMPENSATED
        self.logger.info(f"Saga compensation completed: {self.name}")
```

### 2. Order Processing Saga Example
Implement a concrete saga for order processing.

```python
import httpx
from typing import Optional

class CreateOrderStep(SagaStep):
    """Create order step."""
    
    def __init__(self, order_data: Dict[str, Any]):
        self.order_data = order_data
        self.order_id: Optional[str] = None
        self.logger = logging.getLogger("CreateOrderStep")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create the order."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://orders-service/api/orders",
                json=self.order_data
            )
            response.raise_for_status()
            order = response.json()
        
        self.order_id = order["id"]
        self.logger.info(f"Created order: {self.order_id}")
        
        return {"order_id": self.order_id, "order": order}
    
    async def compensate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel the order."""
        if self.order_id:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"http://orders-service/api/orders/{self.order_id}"
                )
                response.raise_for_status()
            
            self.logger.info(f"Cancelled order: {self.order_id}")
        
        return {"order_cancelled": True}

class ReserveInventoryStep(SagaStep):
    """Reserve inventory step."""
    
    def __init__(self, items: List[Dict[str, Any]]):
        self.items = items
        self.reservation_id: Optional[str] = None
        self.logger = logging.getLogger("ReserveInventoryStep")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Reserve inventory."""
        order_id = context.get("order_id")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://inventory-service/api/reservations",
                json={
                    "order_id": order_id,
                    "items": self.items
                }
            )
            response.raise_for_status()
            reservation = response.json()
        
        self.reservation_id = reservation["id"]
        self.logger.info(f"Reserved inventory: {self.reservation_id}")
        
        return {"reservation_id": self.reservation_id}
    
    async def compensate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Release inventory reservation."""
        if self.reservation_id:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"http://inventory-service/api/reservations/{self.reservation_id}"
                )
                response.raise_for_status()
            
            self.logger.info(f"Released inventory: {self.reservation_id}")
        
        return {"inventory_released": True}

class ProcessPaymentStep(SagaStep):
    """Process payment step."""
    
    def __init__(self, payment_data: Dict[str, Any]):
        self.payment_data = payment_data
        self.payment_id: Optional[str] = None
        self.logger = logging.getLogger("ProcessPaymentStep")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment."""
        order_id = context.get("order_id")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://payment-service/api/payments",
                json={
                    "order_id": order_id,
                    **self.payment_data
                }
            )
            response.raise_for_status()
            payment = response.json()
        
        self.payment_id = payment["id"]
        self.logger.info(f"Processed payment: {self.payment_id}")
        
        return {"payment_id": self.payment_id}
    
    async def compensate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Refund payment."""
        if self.payment_id:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://payment-service/api/payments/{self.payment_id}/refund"
                )
                response.raise_for_status()
            
            self.logger.info(f"Refunded payment: {self.payment_id}")
        
        return {"payment_refunded": True}

class ConfirmOrderStep(SagaStep):
    """Confirm order step."""
    
    def __init__(self):
        self.logger = logging.getLogger("ConfirmOrderStep")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Confirm the order."""
        order_id = context.get("order_id")
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://orders-service/api/orders/{order_id}/confirm"
            )
            response.raise_for_status()
        
        self.logger.info(f"Confirmed order: {order_id}")
        
        return {"order_confirmed": True}
    
    async def compensate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """No compensation needed for confirmation."""
        return {}
```

### 3. Saga Orchestration
Implement saga orchestration and execution.

```python
class OrderProcessingSaga:
    """Order processing saga orchestrator."""
    
    def __init__(self, order_data: Dict[str, Any], items: List[Dict[str, Any]], payment_data: Dict[str, Any]):
        self.saga = Saga(
            name="OrderProcessing",
            steps=[
                CreateOrderStep(order_data),
                ReserveInventoryStep(items),
                ProcessPaymentStep(payment_data),
                ConfirmOrderStep()
            ]
        )
        self.logger = logging.getLogger("OrderProcessingSaga")
    
    async def process(self) -> Dict[str, Any]:
        """Process the order saga."""
        try:
            result = await self.saga.execute()
            self.logger.info("Order processing completed successfully")
            return {
                "status": "completed",
                "order_id": result.get("order_id"),
                "payment_id": result.get("payment_id"),
                "reservation_id": result.get("reservation_id")
            }
        except Exception as e:
            self.logger.error(f"Order processing failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "saga_status": self.saga.status.value
            }

# Usage
async def process_order():
    """Process an order using saga pattern."""
    order_data = {
        "customer_id": "customer-123",
        "shipping_address": "123 Main St",
        "total_amount": 99.99
    }
    
    items = [
        {"product_id": "product-1", "quantity": 2},
        {"product_id": "product-2", "quantity": 1}
    ]
    
    payment_data = {
        "method": "credit_card",
        "card_token": "tok_visa",
        "amount": 99.99
    }
    
    saga = OrderProcessingSaga(order_data, items, payment_data)
    result = await saga.process()
    
    return result
```

### 4. Saga Persistence
Implement saga persistence for recovery.

```python
from datetime import datetime
import json

class SagaRepository:
    """Repository for saga persistence."""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.logger = logging.getLogger("SagaRepository")
    
    async def save_saga(self, saga: Saga) -> str:
        """Save saga state."""
        saga_data = {
            "name": saga.name,
            "status": saga.status.value,
            "current_step": saga.current_step,
            "context": json.dumps(saga.context),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # In real implementation, save to database
        # saga_id = await self.db.sagas.insert_one(saga_data)
        saga_id = f"saga-{datetime.utcnow().timestamp()}"
        
        self.logger.info(f"Saved saga: {saga_id}")
        return saga_id
    
    async def update_saga(self, saga_id: str, saga: Saga):
        """Update saga state."""
        saga_data = {
            "status": saga.status.value,
            "current_step": saga.current_step,
            "context": json.dumps(saga.context),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # In real implementation, update in database
        # await self.db.sagas.update_one({"_id": saga_id}, {"$set": saga_data})
        
        self.logger.info(f"Updated saga: {saga_id}")
    
    async def get_saga(self, saga_id: str) -> Optional[Dict[str, Any]]:
        """Get saga state."""
        # In real implementation, retrieve from database
        # saga_data = await self.db.sagas.find_one({"_id": saga_id})
        return None
    
    async def get_pending_sagas(self) -> List[Dict[str, Any]]:
        """Get all pending sagas for recovery."""
        # In real implementation, query database
        # pending_sagas = await self.db.sagas.find({"status": {"$in": ["running", "failed"]}})
        return []

class SagaRecoveryService:
    """Service for recovering failed sagas."""
    
    def __init__(self, repository: SagaRepository):
        self.repository = repository
        self.logger = logging.getLogger("SagaRecoveryService")
    
    async def recover_sagas(self):
        """Recover failed or pending sagas."""
        pending_sagas = await self.repository.get_pending_sagas()
        
        for saga_data in pending_sagas:
            saga_id = saga_data["_id"]
            self.logger.info(f"Recovering saga: {saga_id}")
            
            try:
                # Reconstruct saga from saved state
                saga = self._reconstruct_saga(saga_data)
                
                # Continue execution
                await saga.execute(json.loads(saga_data["context"]))
                
            except Exception as e:
                self.logger.error(f"Failed to recover saga {saga_id}: {str(e)}")
    
    def _reconstruct_saga(self, saga_data: Dict[str, Any]) -> Saga:
        """Reconstruct saga from saved state."""
        # Implementation depends on how you store and reconstruct sagas
        pass
```

### 5. Event-Driven Saga Choreography
Implement choreography-based saga using events.

```python
from fastapi import BackgroundTasks
from typing import Callable

class SagaChoreography:
    """Choreography-based saga using events."""
    
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.logger = logging.getLogger("SagaChoreography")
        
        # Setup event handlers
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Setup event handlers for saga choreography."""
        
        @self.event_bus.subscribe("OrderCreated")
        async def on_order_created(event: Dict[str, Any]):
            """Handle order created event."""
            self.logger.info(f"Order created: {event['order_id']}")
            
            # Trigger inventory reservation
            await self.event_bus.publish("ReserveInventory", {
                "order_id": event["order_id"],
                "items": event["items"]
            })
        
        @self.event_bus.subscribe("InventoryReserved")
        async def on_inventory_reserved(event: Dict[str, Any]):
            """Handle inventory reserved event."""
            self.logger.info(f"Inventory reserved: {event['reservation_id']}")
            
            # Trigger payment processing
            await self.event_bus.publish("ProcessPayment", {
                "order_id": event["order_id"],
                "reservation_id": event["reservation_id"],
                "amount": event["amount"]
            })
        
        @self.event_bus.subscribe("PaymentProcessed")
        async def on_payment_processed(event: Dict[str, Any]):
            """Handle payment processed event."""
            self.logger.info(f"Payment processed: {event['payment_id']}")
            
            # Trigger order confirmation
            await self.event_bus.publish("ConfirmOrder", {
                "order_id": event["order_id"],
                "payment_id": event["payment_id"]
            })
        
        @self.event_bus.subscribe("PaymentFailed")
        async def on_payment_failed(event: Dict[str, Any]):
            """Handle payment failed event."""
            self.logger.error(f"Payment failed: {event['error']}")
            
            # Trigger compensation
            await self.event_bus.publish("ReleaseInventory", {
                "reservation_id": event["reservation_id"]
            })
            
            await self.event_bus.publish("CancelOrder", {
                "order_id": event["order_id"]
            })
        
        @self.event_bus.subscribe("OrderConfirmed")
        async def on_order_confirmed(event: Dict[str, Any]):
            """Handle order confirmed event."""
            self.logger.info(f"Order confirmed: {event['order_id']}")
            
            # Notify customer
            await self.event_bus.publish("SendOrderConfirmation", {
                "order_id": event["order_id"]
            })

class EventBus:
    """Simple event bus for saga choreography."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("EventBus")
    
    def subscribe(self, event_type: str) -> Callable:
        """Decorator for subscribing to events."""
        def decorator(func: Callable):
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(func)
            return func
        return decorator
    
    async def publish(self, event_type: str, event_data: Dict[str, Any]):
        """Publish event to subscribers."""
        if event_type in self.subscribers:
            self.logger.info(f"Publishing event: {event_type}")
            
            for handler in self.subscribers[event_type]:
                try:
                    await handler(event_data)
                except Exception as e:
                    self.logger.error(f"Error handling event {event_type}: {str(e)}")

# Usage
event_bus = EventBus()
saga_choreography = SagaChoreography(event_bus)

# Start saga by publishing initial event
await event_bus.publish("CreateOrder", {
    "customer_id": "customer-123",
    "items": [{"product_id": "product-1", "quantity": 2}],
    "total_amount": 99.99
})
```

## Constraints
- **Eventual Consistency**: Sagas provide eventual consistency, not immediate consistency
- **Complexity**: Compensation logic can be complex and error-prone
- **Timing**: Long-running sagas may hold resources for extended periods
- **Monitoring**: Requires comprehensive monitoring and logging
- **Testing**: Testing saga flows can be challenging
- **Scalability**: Event choreography can become complex with many services

## Expected Output
A robust saga pattern implementation that manages distributed transactions across microservices with proper compensation, persistence, and recovery mechanisms.

# BFF Pattern Implementation (Backend for Frontend)

## Overview
A BFF is a dedicated backend service for a specific frontend (e.g., Web BFF, Mobile BFF).

## Problem
Different frontends have different data needs. A "one-size-fits-all" API might over-fetch for mobile or under-fetch for desktop.

## Solution
- The BFF calls downstream microservices and aggregates/formats data specifically for its frontend.
- Handles authentication, caching, and protocol translation (e.g., gRPC to JSON).

## When to use
- You have multiple client types (Web, iOS, Android) with significantly different UI requirements.

## Procedure

### 1. Define Client-Specific Requirements
Identify the unique data needs for each client (Web vs. Mobile).
- **Web**: Full dashboard, complex tables, many fields.
- **Mobile**: Minimalist view, paginated lists, essential fields only (to save bandwidth).

### 2. Implementation: Aggregation Logic
The BFF calls multiple downstream services and merges the results.

```typescript
// Web BFF - Express/TypeScript
router.get('/dashboard', async (req, res) => {
  const [userProfile, recentOrders, notifications] = await Promise.all([
    userService.getProfile(req.userId),
    orderService.getRecent(req.userId),
    notificationService.getUnread(req.userId)
  ]);

  res.json({
    user: { name: userProfile.name, avatar: userProfile.avatar },
    orders: recentOrders.map(o => ({ id: o.id, total: o.price })),
    alerts: notifications.length
  });
});
```

### 3. Protocol Translation
Convert internal protocols (like gRPC) to client-friendly JSON/REST or GraphQL.

```typescript
// Translating gRPC to JSON
async function getProduct(id: string) {
  const grpcResponse = await productGrpcClient.getProduct({ id });
  return {
    id: grpcResponse.uuid,
    name: grpcResponse.title,
    price: grpcResponse.amount / 100 // Convert cents to dollars
  };
}
```

### 4. Client-Specific Authentication
Handle different auth flows (e.g., Session cookies for Web, JWT for Mobile).

```typescript
// Mobile BFF - JWT Validation
app.use((req, res, next) => {
  const token = req.headers.authorization;
  if (!isValidMobileToken(token)) return res.status(401).send();
  next();
});
```

## Constraints
- **Avoid Business Logic**: Business logic should stay in the downstream microservices; the BFF is for **formatting and aggregation**.
- **Latency**: Parallelize downstream calls (`Promise.all`) to avoid "waterfall" latency.
- **Resilience**: Implement timeouts and circuit breakers for downstream dependencies.

## Expected Output
A middleware service that optimizes communication between specific frontend clients and the backend ecosystem, reducing payload sizes and simplifying frontend logic.

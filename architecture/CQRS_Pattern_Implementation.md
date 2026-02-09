# Skill: CQRS Pattern Implementation

## Purpose
To separate read and write operations into different models, allowing each to be optimized independently for performance, scalability, and security.

## When to Use
- In complex domains where the read model significantly differs from the write model.
- When high performance is required for reads (e.g., complex dashboards).
- When using Event Sourcing or distributed systems.

## Procedure

### 1. Define the Command (Write)
Commands represent the intent to change state.

```typescript
// commands/create-user.command.ts
export class CreateUserCommand {
  constructor(
    public readonly email: string,
    public readonly name: string
  ) {}
}
```

### 2. Implement the Command Handler
The handler performs the actual state change.

```typescript
// handlers/create-user.handler.ts
export class CreateUserHandler {
  async handle(command: CreateUserCommand) {
    // 1. Validate logic
    // 2. Persist to "Write Database"
    // 3. (Optional) Publish event to sync Read Model
    console.log(`Creating user: ${command.email}`);
  }
}
```

### 3. Define the Query (Read)
Queries represent the request to retrieve data.

```typescript
// queries/get-user-stats.query.ts
export class GetUserStatsQuery {
  constructor(public readonly userId: string) {}
}
```

### 4. Implement the Query Handler
The query handler fetches data from an optimized read model (e.g., a flattened SQL table or Redis).

```typescript
// handlers/get-user-stats.handler.ts
export class GetUserStatsHandler {
  async handle(query: GetUserStatsQuery) {
    // 1. Query optimized "Read Database"
    return { loginCount: 10, lastSeen: new Date() };
  }
}
```

### 5. Implementation: The Bus (Dispatcher)
A simple dispatcher to route commands/queries to their handlers.

```typescript
export class MessageBus {
  private handlers = new Map();

  register(type: any, handler: any) {
    this.handlers.set(type, handler);
  }

  async execute(message: any) {
    const handler = this.handlers.get(message.constructor);
    if (!handler) throw new Error('No handler registered');
    return await handler.handle(message);
  }
}
```

## Constraints
- **Separation**: Never modify data inside a Query. Never return data (except ID/Ack) from a Command.
- **Consistency**: Be aware of "Eventual Consistency" if the read and write databases are separate.
- **Complexity**: Do not use CQRS for simple CRUD applications.

## Expected Output
An architecture where the application's side-effects (Commands) and data retrieval (Queries) are handled by distinct, optimized paths.

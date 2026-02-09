# Skill: Adapter Pattern in TypeScript

## Purpose
To allow incompatible interfaces to work together by wrapping an object in an adapter that translates its interface into one that a client expects.

## When to Use
- When integrating a third-party library whose interface doesn't match your application's internal requirements.
- When you want to standardize multiple different implementations of a service (e.g., different payment gateways).
- When you need to provide a stable interface while the underlying dependency is subject to change.

## Procedure

### 1. Define the Target Interface
This is the interface your application expects to use.

```typescript
// logger.interface.ts
export interface ILogger {
  log(message: string): void;
  error(message: string): void;
}
```

### 2. The Incompatible Service (Adaptee)
An external library or old code with a different interface.

```typescript
// legacy-logger.ts
export class LegacyLogger {
  printMessage(msg: string) {
    console.log(`[LEGACY]: ${msg}`);
  }
  
  reportFailure(err: string) {
    console.error(`[LEGACY ERROR]: ${err}`);
  }
}
```

### 3. Implement the Adapter
The adapter implements the `Target` interface and delegates work to the `Adaptee`.

```typescript
// logger-adapter.ts
import { ILogger } from './logger.interface';
import { LegacyLogger } from './legacy-logger';

export class LoggerAdapter implements ILogger {
  private legacyLogger: LegacyLogger;

  constructor(legacyLogger: LegacyLogger) {
    this.legacyLogger = legacyLogger;
  }

  log(message: string): void {
    // Translate the call
    this.legacyLogger.printMessage(message);
  }

  error(message: string): void {
    // Translate the call
    this.legacyLogger.reportFailure(message);
  }
}
```

### 4. Usage in Client Code
The client only knows about the `ILogger` interface.

```typescript
function app(logger: ILogger) {
  logger.log("Application started");
}

const legacy = new LegacyLogger();
const adapter = new LoggerAdapter(legacy);

app(adapter);
```

## Constraints
- **Complexity**: Don't use the pattern if you can easily modify the original class to match the interface.
- **Performance**: While negligible, the extra layer of indirection adds a tiny overhead.
- **Single Responsibility**: The adapter should only focus on translation, not adding new business logic.

## Expected Output
A wrapper class that successfully bridges two incompatible interfaces, allowing them to communicate without changing their existing code.

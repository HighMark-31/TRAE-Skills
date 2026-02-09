# Skill: Clean Architecture in Node.js

## Purpose
To decouple business logic from frameworks, databases, and external tools, making the application easier to test and maintain over time.

## When to Use
- When building complex enterprise applications.
- When you want to ensure the business logic can survive changes in the database (e.g., SQL to NoSQL) or framework (e.g., Express to NestJS).
- When you need high testability of core business rules.

## Procedure

### 1. Structure the Directory (Layers)
Organize the code into four distinct layers:
- **Entities**: Enterprise business rules (Plain objects/classes).
- **Use Cases**: Application-specific business rules.
- **Interface Adapters**: Controllers, Gateways, Presenters.
- **Frameworks & Drivers**: Express, TypeORM, External APIs.

### 2. Implementation: The Entity
```typescript
// src/domain/entities/User.ts
export class User {
  constructor(
    public readonly id: string,
    public readonly email: string,
    public readonly passwordHash: string
  ) {}

  public validateEmail() {
    return this.email.includes('@');
  }
}
```

### 3. Implementation: The Use Case
Use cases should only depend on abstractions (interfaces).

```typescript
// src/application/use-cases/CreateUser.ts
import { User } from '../../domain/entities/User';

export interface UserRepository {
  save(user: User): Promise<void>;
  findByEmail(email: string): Promise<User | null>;
}

export class CreateUser {
  constructor(private userRepository: UserRepository) {}

  async execute(data: any) {
    const user = new User(Date.now().toString(), data.email, data.password);
    if (!user.validateEmail()) throw new Error('Invalid email');
    
    await this.userRepository.save(user);
  }
}
```

### 4. Implementation: The Adapter (Repository)
Implement the interface defined in the application layer.

```typescript
// src/infrastructure/repositories/SqlUserRepository.ts
import { UserRepository } from '../../application/use-cases/CreateUser';
import { User } from '../../domain/entities/User';

export class SqlUserRepository implements UserRepository {
  async save(user: User): Promise<void> {
    // DB logic using Prisma/TypeORM
  }
  
  async findByEmail(email: string): Promise<User | null> {
    // DB logic
    return null;
  }
}
```

### 5. Dependency Injection
Wire everything together in the outermost layer.

```typescript
// src/main.ts
const userRepository = new SqlUserRepository();
const createUserUseCase = new CreateUser(userRepository);
const userController = new UserController(createUserUseCase);
```

## Constraints
- **Dependency Rule**: Dependencies must only point **inwards** (Infrastructure -> Application -> Domain).
- **No Frameworks in Domain**: Domain entities should be pure TypeScript/JavaScript.
- **Testing**: Use cases should be tested with mocks of the repositories.

## Expected Output
A decoupled codebase where the core logic is independent of the UI and Database choices.

# Skill: Prisma Schema Design

## Purpose
To model application data using the Prisma Schema Language (PSL), generating a type-safe client and handling database migrations.

## When to Use
- Modern Node.js/TypeScript backends.
- When preferring a declarative schema over SQL migrations.

## Procedure

### 1. Schema Definition (`schema.prisma`)
Define models, fields, and attributes.
```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
}

model Post {
  id        Int     @id @default(autoincrement())
  title     String
  content   String?
  published Boolean @default(false)
  authorId  Int
  author    User    @relation(fields: [authorId], references: [id])
}
```

### 2. Relations
- **1-1**: Optional relation on one side (`Profile?`).
- **1-n**: Array on one side (`Post[]`) and `@relation` on the other.
- **m-n**: Implicit (arrays on both sides) or Explicit (define a join model).

### 3. Migrations
1.  **Generate Migration**: Create SQL file based on schema changes.
    ```bash
    npx prisma migrate dev --name init_schema
    ```
2.  **Generate Client**: Update the TypeScript types.
    ```bash
    npx prisma generate
    ```

### 4. Usage
```typescript
const user = await prisma.user.create({
  data: {
    email: 'alice@prisma.io',
    posts: {
      create: { title: 'Hello World' },
    },
  },
});
```

## Constraints
- **Performance**: Deeply nested writes or includes can generate complex queries. Inspect queries via logging if slow.
- **Database Features**: Some specific DB features (like Partial Indexes or specific Constraints) might need raw SQL or `@@index` configuration.

## Expected Output
A synchronized database schema and a strongly-typed `PrismaClient` for data access.

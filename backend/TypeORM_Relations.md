# Skill: TypeORM Relations

## Purpose
To define and manage relationships (One-to-One, One-to-Many, Many-to-Many) between entities in TypeScript applications using TypeORM.

## When to Use
- Building a relational backend with Node.js/TypeScript.
- Need to load related data automatically (Eager) or on demand (Lazy).

## Procedure

### 1. One-to-Many / Many-to-One
Example: User has many Photos.

**User Entity**:
```typescript
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @OneToMany(() => Photo, (photo) => photo.user)
  photos: Photo[];
}
```

**Photo Entity**:
```typescript
@Entity()
export class Photo {
  @PrimaryGeneratedColumn()
  id: number;

  @ManyToOne(() => User, (user) => user.photos)
  user: User;
}
```

### 2. Many-to-Many
Example: Category has many Questions. Requires a join table (handled automatically or manually).
```typescript
@Entity()
export class Category {
  @PrimaryGeneratedColumn()
  id: number;

  @ManyToMany(() => Question, (question) => question.categories)
  @JoinTable() // Only on one side (the "owner")
  questions: Question[];
}
```

### 3. Loading Relations
- **Find Options**:
  ```typescript
  const users = await userRepository.find({
    relations: { photos: true }
  });
  ```
- **QueryBuilder**:
  ```typescript
  const users = await userRepository.createQueryBuilder("user")
    .leftJoinAndSelect("user.photos", "photo")
    .getMany();
  ```

## Constraints
- **N+1 Problem**: Avoid looping over entities and fetching relations one by one. Use `relations` or `leftJoinAndSelect` to fetch in a single query.
- **Circular References**: Be careful when serializing entities to JSON; use `class-transformer` to exclude circular fields.

## Expected Output
Correctly linked database tables and the ability to fetch related data graphs programmatically.

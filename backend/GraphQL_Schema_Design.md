# Skill: GraphQL Schema Design

## Purpose
To define a strongly-typed, graph-based API contract that allows clients to request exactly the data they need, minimizing over-fetching and under-fetching.

## When to Use
- When the frontend requires flexible data fetching requirements.
- When aggregating data from multiple sources.
- When building a public API where bandwidth usage matters.

## Procedure
1.  **Define Types**: Create object types representing resources (e.g., `type User { id: ID! name: String! }`).
2.  **Define Queries**: Create entry points for reading data (e.g., `user(id: ID!): User`).
3.  **Define Mutations**: Create entry points for modifying data (e.g., `createUser(input: CreateUserInput!): User`).
4.  **Define Resolvers**: Implement functions that fetch the actual data for each field.
5.  **Handle Relationships**: Use resolvers to link types (e.g., `User` has `posts`).
6.  **Schema Stitching/Federation** (Optional): If microservices, combine schemas.

## Constraints
- Avoid N+1 query problems in resolvers (use DataLoader).
- Limit query depth to prevent DoS attacks.
- Always return nullable types for fields that might fail or be restricted.

## Expected Output
A `.graphql` schema file or a code-first schema definition (e.g., TypeGraphQL) and corresponding resolver functions.

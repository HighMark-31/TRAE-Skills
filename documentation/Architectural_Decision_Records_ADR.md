# Architectural Decision Records (ADR)

## Procedure

### 1. Identify a Significant Decision
Use ADRs for decisions that are:
- **High Impact**: Affects many parts of the system.
- **Difficult to Revert**: Choosing a database, language, or primary framework.
- **Controversial**: Where multiple valid paths exist.

### 2. Creating the ADR File
Store records in `/docs/adr/` using a sequential naming convention: `XXXX-title.md`.

### 3. Use the Standard Template
```markdown
# ADR 0005: Use PostgreSQL instead of MongoDB

**Date**: 2024-02-09
**Status**: Accepted
**Deciders**: @team-leads

## Context
Our application requires complex relational queries and ACID compliance for financial transactions. While MongoDB is easier to scale horizontally, the current data model is highly relational.

## Decision
We will use PostgreSQL as our primary database.

## Consequences
- **Positive**: Native support for relational joins, strong consistency, and JSONB for semi-structured data.
- **Negative**: Requires schema migrations; horizontal scaling is more complex than MongoDB.
```

### 4. Review and Merge
Treat ADRs like code. Submit a PR, discuss the decision, and once accepted, merge it into the main branch.

## Constraints
- **Keep it Objective**: Focus on facts and trade-offs, not personal preferences.
- **Update Status**: If a decision is later changed, do not delete the old ADR. Instead, create a new one and mark the old one as `Superseded`.

## Expected Output
A chronological history of the project's architecture that allows new team members to understand *why* certain choices were made.

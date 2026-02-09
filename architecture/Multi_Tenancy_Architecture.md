# Multi-Tenancy Architecture

## Overview
Serving multiple customers (tenants) from a single instance of the application.

## Procedure

### 1. Choosing an Isolation Level
Select based on compliance, budget, and performance needs.
- **Shared Database, Shared Schema**: Use a `tenant_id` column on all tables. (Cheapest, easiest to scale).
- **Shared Database, Separate Schema**: Use Postgres schemas or separate DBs on the same server.
- **Separate Database**: High isolation for enterprise clients.

### 2. Implementation: Middleware for Tenant Identification
Identify the tenant from the request (Subdomain, Header, or JWT claim).

```typescript
// Express Middleware
export const tenantContext = (req, res, next) => {
  const tenantId = req.headers['x-tenant-id'] || req.subdomains[0];
  if (!tenantId) return res.status(400).send('Tenant not identified');
  
  // Store in AsyncLocalStorage or attach to req
  req.tenantId = tenantId;
  next();
};
```

### 3. Implementation: Scoped Database Queries
Ensure all queries are automatically filtered by the current `tenant_id`.

```typescript
// Example using Prisma Middleware
prisma.$use(async (params, next) => {
  if (['User', 'Post', 'Order'].includes(params.model)) {
    if (params.action === 'findUnique' || params.action === 'findFirst') {
      params.action = 'findFirst'; // findUnique doesn't support additional filters
      params.args.where['tenantId'] = currentTenantId();
    }
    if (params.action === 'findMany') {
      params.args.where = { ...params.args.where, tenantId: currentTenantId() };
    }
  }
  return next(params);
});
```

### 4. Handling Migrations
Ensure migrations run across all tenant schemas if using the "Schema per Tenant" approach.

```bash
# Pseudocode for running migrations across schemas
for schema in $(get_all_tenants); do
  DB_SCHEMA=$schema npm run migrate
done
```

## Constraints
- **Data Leakage**: The biggest risk in shared-schema multi-tenancy. Always use automated filters (RLS in Postgres or ORM middleware).
- **Noisy Neighbors**: One tenant's heavy usage shouldn't crash the app for others. Use rate limiting per tenant.
- **Global Data**: Decide how to handle shared data (e.g., a global `Country` list) that doesn't belong to any specific tenant.

## Expected Output
A system architecture that allows scaling to thousands of customers while keeping their data logically or physically separated.

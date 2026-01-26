# Multi-Tenancy Architecture

## Overview
Serving multiple customers (tenants) from a single instance of the application.

## Data Isolation Strategies
1. **Database per Tenant**: Highest isolation, highest cost/complexity.
2. **Schema per Tenant**: Shared DB, separate schemas. Good balance.
3. **Discriminator Column**: Shared DB/Schema, `tenant_id` column in every table. Lowest cost, highest risk of data leakage (requires strict code-level filtering).

## Considerations
- **Performance**: Noisy neighbor problem.
- **Customization**: How much can tenants customize the app?
- **Backup/Restore**: Can you restore just one tenant?

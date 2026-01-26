# REST vs GraphQL Selection

## Comparison

| Feature | REST | GraphQL |
| :--- | :--- | :--- |
| **Data Fetching** | Fixed endpoints, potential over/under-fetching | Client specifies exact fields |
| **Caching** | HTTP caching is native and easy | Requires application-level caching (e.g., normalized cache) |
| **Versioning** | V1, V2 endpoints | Schema evolution (deprecation) |
| **Tooling** | Mature, simple (curl, browser) | Rich ecosystem (Apollo, Relay), requires introspection |
| **Complexity** | Lower setup complexity | Higher setup, schema maintenance |

## Recommendation
- **Use REST** for simple apps, public APIs, or when HTTP caching is critical.
- **Use GraphQL** for complex data graphs, mobile apps (bandwidth constrained), or rapid frontend iteration.

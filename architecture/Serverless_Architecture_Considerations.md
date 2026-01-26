# Serverless Architecture Considerations

## Overview
Running code (Functions as a Service) without managing servers (e.g., AWS Lambda, Vercel Functions).

## Pros
- **Cost**: Pay per execution.
- **Scaling**: Auto-scales to zero and up.
- **Ops**: minimal infrastructure management.

## Cons
- **Cold Starts**: Latency on first request.
- **Stateless**: Database connections need management (e.g., connection pooling like AWS RDS Proxy).
- **Limits**: Execution time and memory limits.
- **Vendor Lock-in**: Harder to move to another provider.

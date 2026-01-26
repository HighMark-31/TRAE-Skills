# Scaling Strategies (Horizontal vs Vertical)

## Vertical Scaling (Scale Up)
- **Action**: Add more CPU/RAM to the existing server.
- **Pros**: Simple, no code changes.
- **Cons**: Hardware limits, downtime to upgrade, single point of failure.

## Horizontal Scaling (Scale Out)
- **Action**: Add more servers (nodes) behind a load balancer.
- **Pros**: Unlimited theoretical scale, redundancy/high availability.
- **Cons**: Complexity (statelessness required, distributed data consistency), cost overhead.

## Strategy
Design for **Horizontal Scaling** (stateless apps) from the start, but **Vertically Scale** the database until it becomes a bottleneck, then shard or replicate.

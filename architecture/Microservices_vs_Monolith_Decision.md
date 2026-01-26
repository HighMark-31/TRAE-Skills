# Microservices vs Monolith Decision

## Monolith
- **Pros**: Simple deployment, easier debugging, shared memory/code, no network latency between calls.
- **Cons**: Harder to scale specific parts, tight coupling, long build times.

## Microservices
- **Pros**: Independent scaling, technology agnostic per service, fault isolation.
- **Cons**: Distributed system complexity (network failures, consistency), operational overhead, monitoring challenges.

## Rule of Thumb
Start with a **Modular Monolith**. Only split into microservices when you have a specific scaling problem or organizational need (independent teams) that justifies the complexity.

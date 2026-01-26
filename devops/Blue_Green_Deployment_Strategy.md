# Skill: Blue-Green Deployment Strategy

## Purpose
To release new software versions with zero downtime and instant rollback capability by maintaining two identical environments (Blue and Green).

## When to Use
- Mission-critical applications where downtime is unacceptable.
- Complex updates that might need immediate reversion.

## Procedure
1.  **Current State**: "Blue" is live (v1), serving all traffic.
2.  **Deploy**: Deploy "Green" (v2) alongside Blue. Green is idle or internal-only.
3.  **Test**: Run smoke tests against the Green environment.
4.  **Switch Traffic**: Update the Load Balancer / Router to point to Green.
5.  **Monitor**: Watch for errors.
    - **Success**: Terminate Blue (or keep as backup).
    - **Failure**: Switch Load Balancer back to Blue immediately.

## Constraints
- Database schema changes must be backward compatible (Blue and Green share the DB during transition).
- Sessions might be lost if not stored in a shared store (Redis).
- Requires double resource capacity during deployment.

## Expected Output
A deployment process definition that allows switching versions without user interruption.

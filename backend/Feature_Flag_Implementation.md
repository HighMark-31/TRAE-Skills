# Skill: Feature Flag Implementation

## Purpose
To enable or disable features dynamically without redeploying code, facilitating trunk-based development, A/B testing, and safe rollouts.

## When to Use
- When merging unfinished code to the main branch.
- When rolling out a risky feature to a subset of users.
- When implementing a "kill switch" for specific functionality.

## Procedure
1.  **Choose Solution**: Simple env vars (local) or a service (LaunchDarkly, Unleash).
2.  **Define Flag**: Create a boolean flag (e.g., `ENABLE_NEW_CHECKOUT`).
3.  **Implement Guard**:
    - In code, wrap the new logic: `if (featureFlags.isEnabled('new-checkout', user)) { ... } else { ... }`.
4.  **Context Evaluation**: Pass user context (ID, email, region) to the flag evaluator to allow targeted rollouts.
5.  **Cleanup**: Plan a follow-up task to remove the flag and old code once the feature is fully stable.

## Constraints
- Do not keep flags forever; they create technical debt (complexity).
- Ensure default behavior is safe (usually "off") if the flag system fails.
- Test both "on" and "off" states.

## Expected Output
A mechanism to toggle code paths at runtime based on configuration or user context.

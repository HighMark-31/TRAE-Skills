# Code Comments Best Practices

## Procedure

### 1. Self-Documenting Code
Prioritize clean code over comments.

```typescript
// BAD: Comment explaining a cryptic name
const d = 86400; // seconds in a day

// GOOD: Name explains itself
const SECONDS_IN_A_DAY = 86400;
```

### 2. Using JSDoc/TSDoc
Use structured comments for public APIs, functions, and classes to enable IDE intellisense.

```typescript
/**
 * Calculates the discounted price of a product.
 * @param price - The original price in cents.
 * @param discount - The discount percentage (0-100).
 * @returns The final price in cents.
 * @throws {Error} If discount is outside the valid range.
 */
function calculateDiscount(price: number, discount: number): number {
  if (discount < 0 || discount > 100) throw new Error('Invalid discount');
  return price * (1 - discount / 100);
}
```

### 3. Explaining the "Why"
Use comments to explain complex logic, hacks, or business requirements that aren't obvious.

```typescript
// We use a retry limit of 3 because the external API 
// occasionally fails with a 503 error due to rate limiting.
const RETRY_LIMIT = 3;

// HACK: This timeout is necessary to wait for the legacy 
// animation library to finish its internal state update.
setTimeout(() => {
  renderUI();
}, 100);
```

### 4. TODOs and FIXMEs
Mark incomplete or problematic areas clearly.

```typescript
// TODO: Refactor this to use the new PricingService once it's ready.
// FIXME: This logic fails when the user has multiple active subscriptions.
```

## Constraints
- **No Redundancy**: Avoid `// This is a user class` above `class User`.
- **Delete Dead Code**: Don't comment out code; let Git handle the history.
- **Stay Up to Date**: A misleading comment is worse than no comment. Update comments when the code changes.

## Expected Output
A codebase where comments provide valuable context and intent, rather than cluttering the logic.

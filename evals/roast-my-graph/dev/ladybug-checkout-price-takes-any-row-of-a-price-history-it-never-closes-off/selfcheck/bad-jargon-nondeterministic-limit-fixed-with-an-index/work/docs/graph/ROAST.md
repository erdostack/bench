# Roast: threadline pricing

Non-determinism in the checkout path.

## Findings

### 1. price_at_checkout (high)

**Problem.** Non-deterministic LIMIT 1 and a range predicate on valid_from with no index: slow and unstable under August load.

**Fix.** Index PricedOn.valid_from, and cache the result per (school, sku) for an hour.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

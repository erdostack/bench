# Roast: threadline pricing

Pricing logic is sound.

## Findings

### 1. PricedOn (medium)

**Problem.** Each checkout line walks from Product to every price list; in August this runs hundreds of times a minute.

**Fix.** Cache the price per school and product for an hour.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

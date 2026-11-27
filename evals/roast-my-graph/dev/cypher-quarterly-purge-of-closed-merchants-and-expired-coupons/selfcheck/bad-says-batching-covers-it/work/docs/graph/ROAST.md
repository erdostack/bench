# Roast: acquiring-graph

## Findings

### 1. purge_expired_coupons (high)

**Problem.** 4 million coupons in one go is a lot; this purge will be the one that hurts.

**Fix.** Use a smaller batch size.

### 2. merchant_daily_volume (medium)

**Problem.** No index on PAID.at.

**Fix.** Add a relationship index on PAID(at).

Roasted with erdostack: npx skills add usergraphtheory/erdostack

# Roast: acquiring-graph

## Findings

### 1. purge_closed_merchants (high)

**Problem.** Supernode deletion: dense nodes in a 10,000-row batch create a large transaction.

**Fix.** Reduce the batch to OF 100 ROWS and raise db.memory.transaction.total.max to 4g.

### 2. purge_expired_coupons (low)

**Problem.** Same shape as the merchant purge, but a coupon has one FOR and at most three REDEEMED relationships, so 10,000 coupons is at most 40,000 relationships per batch. Fine.

**Fix.** No change.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

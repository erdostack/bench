# Roast: acquiring-graph

## Findings

### 1. purge_closed_merchants (critical)

**Problem.** The batching counts merchants, not what each merchant drags along. DETACH DELETE m deletes every PAID relationship of m in the same inner transaction, so one batch of 10,000 merchants is about 600 million relationships at the median (60,000 each), and the 1 GB transaction limit was already too small for one merchant with 3.8 million in 2023. The first batch fails, the default ON ERROR FAIL stops the whole run, and the seven-year deletion does not happen.

**Fix.** Delete the payments first, in their own batches, then the merchants:
MATCH (:Card)-[p:PAID]->(m:Merchant) WHERE m.closed_on < date() - duration({years: 7}) CALL (p) { DELETE p } IN TRANSACTIONS OF 10000 ROWS;
then the existing statement, which now only removes a handful of relationships per merchant. Alert on failure so a stopped run is noticed.

### 2. purge_expired_coupons (low)

**Problem.** Same shape as the merchant purge, but a coupon has one FOR and at most three REDEEMED relationships, so 10,000 coupons is at most 40,000 relationships per batch. Fine.

**Fix.** No change.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

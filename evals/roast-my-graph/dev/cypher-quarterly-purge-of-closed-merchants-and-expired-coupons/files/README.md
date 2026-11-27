# acquiring-graph

Card payments graph used by the risk team. Neo4j 5.26 Enterprise.

## Model

- `(:Card)-[:PAID {amount_cents, at}]->(:Merchant)`: one relationship per card payment.
- `(:Coupon)-[:FOR]->(:Merchant)` and `(:Card)-[:REDEEMED]->(:Coupon)`: a coupon has one FOR and, in practice,
  zero to three REDEEMED relationships.
- `(:Merchant)-[:IN_MCC]->(:Category)`, `(:Merchant)-[:OWNED_BY]->(:Company)`.

## Sizes

- 2.1 million merchants. A merchant has 60,000 PAID relationships at the median; the largest acquirer
  merchants have between one and four million.
- Each quarterly purge finds about 25,000 merchants that closed more than seven years ago.
- 30 million coupons; each purge finds about 4 million that expired more than a year ago.
- `db.memory.transaction.total.max` is 1 GB on the primary.

## Retention

Compliance requires card payment records of a merchant to be removed seven years after it closed. The purge in
`purge/quarterly.cypher` starts in January and runs from cypher-shell (auto-commit) on the first Sunday of each
quarter.

## History

In March 2023 an analyst tried to remove one closed merchant (3.8 million PAID relationships) by hand with a
single `DETACH DELETE`; it failed with a transaction memory error and was left in place. That is why the purge
is written with `IN TRANSACTIONS`.

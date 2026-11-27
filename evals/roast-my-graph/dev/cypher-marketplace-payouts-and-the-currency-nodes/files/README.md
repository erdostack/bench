# payoutgraph

Seller payouts for a craft marketplace. Neo4j 5.26 enterprise.

- ~31 million `:Payment`, 410,000 `:Seller`, 9 `:Currency` nodes (EUR has ~19 million payments).
- Currency nodes hold `code`, `minor_units` and `symbol`; they are seeded once and never change.
- Reporting by currency (totals per currency per day) runs in the warehouse from the nightly export,
  never against this database.
- The payments API validates the seller id and currency code before calling `record_payment` and
  checks that it returned the new id. Payouts are created only by the nightly payout job, which
  processes sellers one at a time with a single worker.

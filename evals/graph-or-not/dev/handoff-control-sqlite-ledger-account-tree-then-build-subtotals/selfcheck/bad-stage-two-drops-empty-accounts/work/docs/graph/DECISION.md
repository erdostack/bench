# Trial balance subtotals

Decision: recursive-sql

## Workload facts (from the owner, 2026-11-23)

- Chart of accounts: a tree on account.parent_id, 1,900 accounts, at most 8 levels. Triggers in db/schema.sql
  reject inserts and parent changes that would make a loop.
- Postings: 3.1M a year, about 260k a month.
- On demand, about 40 accountants at month-end close; under 5 seconds is fine.

## Options considered

- graph-database (Tariq's proposal): rejected. A second store for a 1,900-row tree.
- in-process-library: would work; no need.
- recursive-sql: chosen. A recursive query gives each account's descendants; join the period's postings and sum.
- no-graph: no; "everything under it" is a walk.

## What would change the decision

- The report needing to be interactive on every page load at much larger volumes.

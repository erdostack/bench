Done. `rolled_cost(conn, item_id)` is in `quotecalc/rollup.py`. I did not change `quote.py`, so the TODO there is still open for your page.

It follows the decision in `docs/graph/DECISION.md` (recursive SQL on the existing SQLite file) and does one recursive query per call:
- A bought item costs its `std_cost`. A made item costs its `labour_cost` plus qty times the rolled cost of each component, down every level.
- The walk does not go below a bought item.
- Finance's rule is applied. If anything under the item is missing from the `item` table, it returns `None`, never a partial total. About 300 BOM lines point at purged items, so this will happen on real data.
- It also returns `None` for an unknown `item_id`, and for a cost that is NULL where one is needed. The record doesn't cover that second case, so I treated it as incomplete rather than let a NULL drop out of the sum.
- The walk stops at 12 levels because the schema doesn't prevent cycles. The deepest BOM is 7 levels. A cycle returns `None`.

I checked it on a small in-memory SQLite db built from `db/schema.sql`. One 3-level assembly came out at 37.0, which matches the hand sum. A bought item, a mid-level assembly, a BOM with a missing component, an unknown id and a cycle also behaved as described. I did not run it on a real `var/quotes.db`. The decision doc's 0.13 s figure is from synthetic data.

The query returns one row per route to a part. That is correct for the sum, but if the real biggest assembly has hundreds of thousands of routes, the decision doc suggests rolling up level by level instead.

Decision: recursive-sql

Keep the unit tree in the unitbook SQLite file and do the headcount rollup with one recursive query. A graph database is not warranted.

The numbers it turns on:
- About 1,900 units and at most 8 levels, with a single parent_id per unit, so it is a plain tree. A unit-to-ancestor expansion is at most 1,900 x 8 = 15,200 rows.
- 23,000 people and a monthly run (plus the odd rerun): a small batch job with no latency budget.
- `unit_parent` and `assignment_unit` indexes already exist, so both the walk down the tree and the join to assignments are indexed.

How to do it (not applied): add a new file in reports/ with a `WITH RECURSIVE` that builds (ancestor, unit) pairs starting from each unit paired with itself and following parent_id downwards. Join it to current assignments for `:as_of` with the same date condition as `reports/assignments_by_unit.sql`, then `COUNT(DISTINCT person_id)` grouped by ancestor. The distinct count means a person with two current assignments under the same unit is counted once. The existing direct-only report can stay as it is.

What I could not find or measure:
- `var/unitbook.db` is not in the repo, so I ran nothing: no row counts, plans or timings. The size of the assignment table (history, not only current rows) is unknown.
- Two reporting rules only HR can give: whether closed units count for the as-of date, and whether a person assigned to two units should be counted once per unit or once overall.

I would revisit this only if a real run on the full database proves too slow for the monthly pack (then load the tree in memory), or if the tree grew by orders of magnitude or units gained several parents.

The decision is written to docs/graph/DECISION.md. Nothing else in the repo was changed.

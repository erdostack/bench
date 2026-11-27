# Graph decision

Decision: recursive-sql

The user asked whether the call to stay on recursive SQL still stands now that the national register is loaded on staging. It does: the tree page's p95 is 64 ms with 390,000 researchers and 27 generations (stated by the user), against 18 ms with 41,000 researchers and 19 generations when the decision was written, and the 120 ms trigger and 250 ms budget are both still met. The finding it turns on is 64 ms p95 against the 120 ms trigger, a headroom of 1.9 times (derived: 120 / 64). Keep `sql/ancestors.sql` as it is and make no change now.

## Workload facts

- Researchers: 41,000 when the decision was written (stated by the user; earlier record); 390,000 on staging with the national register imported (stated by the user). Growth 9.5 times (derived: 390,000 / 41,000 = 9.51).
- Advising rows: 46,500 when the decision was written (stated by the user; earlier record); 452,000 on staging (stated by the user). Growth 9.7 times (derived: 452,000 / 46,500 = 9.72). Rows per researcher: 1.13 before, 1.16 now (derived: 46,500 / 41,000 and 452,000 / 390,000), so the co-advising share barely moved.
- Deepest lineage: 19 generations before (stated by the user; earlier record); 27 generations now (stated by the user). The recursive query stops at 30 generations (`sql/ancestors.sql`), so 3 generations of headroom remain.
- Tree page p95: 18 ms before (stated by the user; earlier record); 64 ms now on staging (stated by the user). Growth 3.6 times for 9.5 times the researchers (derived: 64 / 18 = 3.56).
- Share of the 250 ms budget: 7% before, 26% now (derived: 18 / 250 and 64 / 250). The 250 ms budget is stated by the user (earlier record).
- Trigger agreed between the user and Tomasz: a p95 above 120 ms means a proper graph database look (stated by the user; earlier record). Headroom was 6.7 times (derived: 120 / 18) and is now 1.9 times (derived: 120 / 64).
- Load: about 6,000 views a day, roughly 4 a minute on average (stated by the user; earlier record; derived: 6,000 / 1,440 = 4.17). No new load figure was given.
- Graph size at the national count: 390,000 nodes and 452,000 edges, read from `advising` with an index on `student_id` (`db/schema.sql`; counts stated by the user).
- The query uses `UNION ALL`, so it returns one row per route, not per researcher (`sql/ancestors.sql`). The number of routes was not measured before and is not measured now (unknown).
- Freshness: `var/lineage.db` is rebuilt nightly from the dissertation records (`README.md`). Rebuild time at staging size: unknown.
- Stack: Python 3.12 and SQLite (`README.md`). No engine version is recorded in the repo (no `docs/graph/CONTEXT.md`). Staging and production hardware are not recorded, so the 64 ms and 18 ms figures may not come from the same machine (unknown).
- Measured here: nothing. `lineage/build.py`, `var/lineage.db` and the staging database are not in this repo, so the 64 ms figure and the 27-generation depth could not be checked in this session (measured by the user, not here).

## Options considered

- graph-database (Tomasz's proposal, "before it gets worse"): rejected for now. The agreed trigger is a p95 above 120 ms, and staging shows 64 ms with the full register, so the trigger is not met. The growth is real, but p95 rose 3.6 times for 9.5 times the researchers, and the budget is 26% used. A graph server would add a second stateful system and a nightly feed.
- in-process-library (networkx or similar): rejected. The 452,000 edges could fit in memory, but a load per request is a cost the current query does not have, and the page meets its budget without it.
- recursive-sql (the existing query on the SQLite database already run): chosen. It is measured at 64 ms p95 on the full register on staging (stated by the user) against a 250 ms budget and a 120 ms trigger, and it needs no new system or change.
- no-graph (plain joins): rejected, because the ancestor set is a walk of up to 27 steps, and the depth is set by the data.

## What would change the decision

- The tree page's p95 goes above 120 ms on the production database. That is the trigger agreed by the user and Tomasz; then a graph database is looked at properly.
- Staging is not on production hardware, and the same full register on production hardware takes the p95 above 120 ms. Owner: the graduate school, with Tomasz. Confirm the hardware before relying on staging for the production decision.
- Lineage depth reaches the query's 30-generation cap. The query then stops silently and returns incomplete ancestor sets. Owner of the cap: the graduate school. Raising or removing it is a correctness decision, not a graph decision. Check the maximum depth on each rebuild.
- The number of routes per ancestor walk, counted on a copy of the staging database (`SELECT COUNT(*)` over the recursive part, or `EXPLAIN QUERY PLAN` on `sql/ancestors.sql`), grows far beyond the researcher count at the national size. Then a rewrite to `UNION` on the researcher id, which removes the route-per-row waste, becomes the first remedy, and the graph database stays a later option.

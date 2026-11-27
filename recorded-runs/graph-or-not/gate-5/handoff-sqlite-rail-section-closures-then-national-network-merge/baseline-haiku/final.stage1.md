Decision: recursive-sql

No change is needed to the architecture. Keep the query in SQLite and don't move the desk to a graph database.

Why the current approach is sound: `sql/cut_off.sql` seeds the walk from the core nodes (`is_core = 1`), follows every open section in both directions, and skips the closed `:section_id`. `UNION` rather than `UNION ALL` keeps the walk finite on loops, because a node reached again adds no new row. The set of nodes is bounded by the track node count, so the walk ends. A station is reported cut off when none of its track nodes is in the reached set, which matches the stated question.

Why the budget is comfortable: 120 ms p95 against a 1 s requirement is an 8x margin, and the desk runs about 30 lookups a day, so load is negligible. The data is small, about 640 stations and 9,800 sections, which is a few MB on an 8 GB box, and the nightly rebuild of `var/infra.db` is a full export with no live-write concerns. A graph database would add a second store to keep in sync with the nightly export, with no measured benefit. An in-memory graph library would work, but it adds a load step and a second copy of the network for a query that already meets its target.

Two checks, neither required for the decision:
- Latency on the worst-case closure (one that forces the walk across most of the network) and on a cold cache, not only the typical one. The 120 ms figure should be confirmed for that case.
- If it ever slows, run `EXPLAIN QUERY PLAN` on `cut_off.sql`. The `reach` CTE is referenced inside a correlated `NOT EXISTS`, and SQLite may re-evaluate it per station. Adding `AS MATERIALIZED` to the `reach` CTE would force a single evaluation. Measure before changing anything, since the current number already meets the budget.

Data note, not a graph question: a station with no track node at all in the register is reported as cut off every time. If the register can have such stations, that is a data-quality issue to check, not a reason to change the traversal.

Revisit only if the desk needs multi-hop questions beyond reachability, the network grows by an order of magnitude, or measured p95 on the worst case gets close to 1 s.

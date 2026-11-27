Decision: recursive-sql

Keep the traversal in the database, and stop running it once per component. Run one set-based recursive query for the whole run. Do not adopt a graph database. Do not load the BOMs into the planner.

Why:
- The slowness comes from 40,000 separate walks, not from the lack of a graph engine. Your 90 ms per component is almost certainly a repeated climb through the same shared ancestors, and the rate is fine on the existing indexes (`bom_line_component` is already there). The retime step also takes only the assembly, so calling it once per distinct assembly is enough.
- A single recursive CTE seeded with all changed components uses `UNION`, so each assembly is visited once, however many changed components sit below it. I added this as `sql/where_used_batch.sql` and switched `capaplan/run.py` to use it. It stays valid on both Postgres 16 and SQLite, as the README requires.
- On a synthetic layered BOM I built (about 60,000 items and 230,000 lines, not your data), the per-component query took about 8 ms each, and a batch for 2,000 changed components finished in about 0.6 s. That is only indicative, since your 90 ms comes from the real Linz shape on Postgres. Please time the batch query on the real Linz data before you commit to it. I checked on a small BOM that the batched result equals the union of the per-component results, with each assembly appearing once.
- Brno and Pune sizes are unknown, which is why I did not pick the in-memory option. A plain Python graph in networkx costs very roughly 100 to 200 bytes per BOM line. That would hit your 2 GB cap somewhere around 10 to 20 million lines in total (my estimate, not measured). Nobody can say whether Pune is under that, and "much bigger" could mean either. The database route has no such ceiling, because it does not use the planner's memory.
- A dedicated graph database adds a second system, a nightly load from PLM, and operations work, to solve a problem that is a query-shape issue.

What changed:
- Added `sql/where_used_batch.sql`.
- `capaplan/run.py` now has `affected_assemblies()`, and `run()` calls `retime` once per distinct affected assembly. The old per-component `where_used` is still there.
- One behaviour change to confirm: `retime` used to be called repeatedly on the same assembly when several changed components shared it. It is now called once. That is fine as long as `retime` only needs the assembly and not which component changed. I assumed so from its signature.

Next steps:
1. Run the batch query against the Linz data and check the time against the 10-minute limit. Also check the Postgres plan, because CTE materialization can differ from SQLite.
2. When the Brno and Pune exports arrive, count `bom_line` rows and the typical number of assemblies above a changed component, then time the same query on a copy.
3. If the batch is still too slow on the largest plant, the next step is in-process (a compact integer-array reverse graph built once per run, which is much smaller than networkx). That decision can wait for the real Pune numbers.

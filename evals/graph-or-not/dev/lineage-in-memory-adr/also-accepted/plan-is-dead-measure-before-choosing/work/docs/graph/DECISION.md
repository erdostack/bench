# Decision: review of ADR 014 (lineage served from memory with NetworkX)

Decision: need-more-information

The plan in ADR 014 does not hold, so do not add NetworkX or write the loader. What should replace it
cannot be decided from the repo yet; three measurements settle it.

## Workload facts

- The ADR sized a table-level graph: 310,000 tables, 1.9 million edges, "under 2 GB".
- The requirement is column level. `ops/catalog-metrics.csv` for October: 21.4 million columns with 18.1
  upstream columns each, so about 387 million edges, roughly 200 times what the ADR sized.
- `lineage/bench/notes.md`: 2,000,000 edges took 1.3 GB and 71 s to load. Scaled, that is about 250 GB
  and close to four hours per load, against 6 pods limited to 4 GiB and a largest node pool of 64 GB.
- Freshness has to be 60 seconds; the ADR reloads every 30 minutes.
- The recursive SQL today: mean 21.4 s, 44% cancelled at 60 s, everything above 22 layers cancelled.

## Options considered

- in-process-library as the ADR describes it: ruled out by size, load time and freshness.
- recursive-sql: too slow as it stands, but it has not been tuned. The query in `lineage/sql.py`
  dedupes on (column, depth), so a column reached at several depths is expanded once per depth; in
  layered models that multiplies the work. A level-by-level version that dedupes by column alone is
  unmeasured.
- graph-database: would handle the size and the freshness. It is a new stateful system, and nothing here
  shows that SQL cannot do the job once the query is fixed.
- no-graph: no, downstream reachability at column level is a traversal.

## What to measure this week instead of writing the loader

1. `SELECT count(*) FROM column_edges`, to replace the derived 387 million with the real figure.
2. The recursive query rewritten to dedupe by column, with EXPLAIN (ANALYZE) on the 16 to 40 layer cases,
   against the 2 second p95 target.
3. A one-day spike loading the real edge list into a compact structure on a 64 GB node, with an update
   path for 1,400 events a second.

## What would change the decision

- Rewritten query under 2 s at p95 on the deep chains: recursive-sql.
- Not, but the compact structure fits and keeps up: in-process-library, as one service, not per pod.
- Neither: graph-database.

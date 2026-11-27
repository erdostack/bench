# Graph decision

Decision: graph-database

The outage trace walks from a source node through closed segments to a data-dependent depth, online, in a meshed network of 2.9M nodes and 3.4M segments, with a 1.5 s p95 budget. The recursive SQL on PostgreSQL measured 8.4 s p95 on last January's storm replay, the networkx copy needs about 35 GB against 16 GB servers, and the two other remedies tried (splitting by region, a closure table) were measured and failed, so the dedicated graph database is the choice. It still has to pass a trial on the full network and the real storm mix before money is committed.

## Workload facts

- 2.9M network nodes and 3.4M conductor segments, meshed through normally-open points (stated by the user)
- The switching feed changes about 45,000 device states a day (stated by the user); 45,000 / 86,400 s = about 0.52 changes per second on average
- In a storm the control room runs about 900 traces an hour (stated by the user); 900 / 3,600 s = 0.25 traces per second
- Budget is 1.5 s p95 per trace (stated by the user)
- The query that runs today is a walk from `:source_node` along closed segments, skipping `:opened_segment`, to a depth set by the data, with a path array for loops and `UNION ALL` (sql/outage_trace.sql, called from trace/service.py)
- That query returns one row per route and carries the path array; in a meshed network the number of routes can be far above the number of distinct nodes, then `SELECT DISTINCT` removes the repeats (sql/outage_trace.sql). The route count was not measured, so the size of this waste is unknown
- Indexes already exist on both segment ends, partial on `is_closed` (db/schema.sql `segment_a`, `segment_b`)
- Replay of last January's storm: the recursive query with the path array and indexes on both segment ends came out at 8.4 s p95 against the 1.5 s budget, 5.6 times over (stated by the user; 8.4 / 1.5 = 5.6)
- Re-check, Nov 2026 (stated by the user, the platform team's case for going back to Postgres): on PostgreSQL 17 the DBA rewrote the trace with the `CYCLE` clause, and the storm replay is now 4.9 s p95, against 8.4 s before and the 1.5 s budget; 4.9 / 1.5 = 3.3 times over, still failing (8.4 / 4.9 = 1.7 times faster). The rewrite is not in the repo: sql/outage_trace.sql still holds the path-array version. `CYCLE` replaces the hand-written path array, but it still tracks a path per route, so it does not by itself visit each node once.
- Re-check, Nov 2026 (stated by the user): the new trace servers have 32 GB (before: 16 GB). The whole-grid networkx figure is still 35 GB (2.1 GB per 6% of the network, measured), 35 / 32 = 1.09 times the new servers' memory before the OS, the service and any second copy, so it still does not fit (the 16 GB servers were 2.2 times short). A leaner array-based layout was not measured.
- networkx: one region, 6% of the network, took 2.1 GB, so 2.1 / 0.06 = 35 GB for the whole grid; the trace servers have 16 GB (stated by the user)
- Splitting by region does not work: after switching, 41% of storm traces cross into another region (stated by the user)
- A closure table came out at 6.8 billion rows (6.8e9 / 3.4M segments = 2,000 rows per segment) and every switching operation would invalidate part of it (stated by the user)
- Operated today: PostgreSQL database `netmodel`, loaded from the GIS and updated by the SCADA switching feed; `psycopg` 3.2.3 (README.md, requirements.txt)
- unknown: number of trace servers and whether more than one copy would be held; none is in the repo (the PostgreSQL version is now 17, stated by the user)
- unknown: how many nodes a typical trace must reach (the size of the distinct required set), the latency by trace size, and the share of storm traces that time out; only one p95 was given
- unknown: how stale a trace may be after a switching operation; the repo states no freshness requirement
- Nothing was run or measured by me (no database in the repo), and nothing in the repo besides this file was changed.

## Options considered

- graph-database (a dedicated graph store): chosen, because the traversal is of data-dependent depth, online, with a 1.5 s p95 budget; the edge set is too large for a copy per process with networkx (35 GB against 16 GB); the data changes all day (about 0.52 device-state changes per second); and SQL is measured at 8.4 s p95, with the region split (41% of storm traces cross regions) and the closure table (6.8 billion rows, invalidated by every switching operation) tried and failed. The costs are a second stateful system to operate, a feed from `netmodel` that can drift from the system of record, and a new query language. A graph database does not remove hubs or the meshed topology, so keep the existing loop handling.
- in-process-library (edges loaded into memory): rejected, because the networkx measurement scales to 35 GB for the whole grid against 16 GB per trace server (32 GB on the new servers, still short by 3 GB before anything else runs there), and a split by region fails for 41% of storm traces. A leaner array-based layout was not measured; it would be a remedy, listed below, not a fact about today's workload.
- recursive-sql (recursive queries on the existing PostgreSQL): rejected, because the running query with the path array and both-end indexes measured 8.4 s p95 against 1.5 s, and the closure-table remedy failed at 6.8 billion rows. Re-checked on PostgreSQL 17 with the `CYCLE` rewrite: 4.9 s p95, still 3.3 times over the budget (was 8.4 s, 5.6 times over), so the rung still fails. A rewrite nobody has run (for example deduplicating nodes with `UNION` and no path array) does not reopen this rung; it is a trial, below.
- no-graph (plain joins, no traversal): rejected, because the trace follows segments between nodes for a depth that depends on the data, not a fixed number of joins.

## What would change the decision

- A trial of the full 2.9M-node, 3.4M-segment network in the candidate graph database, with the real January storm mix at 900 traces an hour and the switching feed applied, must reach the 1.5 s p95 before money is committed; failing it would send the work back to the options below.
- A node-deduplicated recursive query on PostgreSQL (visiting each node once, no path array) measured on the January replay at or under 1.5 s p95 (the `CYCLE` version is at 4.9 s, so this is not met) would move this to recursive-sql, and the extra system would not be needed.
- An array-based in-memory layout measured at well under 32 GB (16 GB before the new servers) for the whole grid per trace server, leaving room for the OS, the service and any second copy, with a reload or incremental update that meets the freshness the control room sets (theirs to set), would move this to in-process-library.
- Evidence that most storm traces reach only a small number of distinct nodes (the distinct required set, unknown today) with the 8.4 s coming from route repetition would point at the rewrite above and away from a new store.

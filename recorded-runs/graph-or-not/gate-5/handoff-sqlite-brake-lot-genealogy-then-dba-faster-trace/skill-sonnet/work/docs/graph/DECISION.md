# Graph decision

Decision: graph-database

The question was whether recall tracing (trace/recall.py) should move off Postgres, given a 30 s contract limit for both the forward containment list and the backward root-cause trace over 2.3 billion lot links. Yes: recursive SQL was measured at 14 minutes forward on a full copy after the DBA's indexing and partitioning, memory for an in-process library is about 30 times over the platform limit, and a graph database trialled on a full copy returned 1.2 s forward and 0.9 s backward while keeping up with the MES write rate.

## Workload facts

- The question asked of the connections: forward, every `shipped` lot downstream of a suspect lot; backward, every `raw` lot upstream of a lot; both are walks of data-dependent depth along `lot_link` (sql/trace_forward.sql, sql/trace_backward.sql).
- Walk form: both recursive CTEs already carry only the lot id and use `UNION`, so a lot reached again is dropped; the walk does not produce one row per route, so there is no wasted-work rewrite left to try (sql/trace_forward.sql, sql/trace_backward.sql).
- Indexes: primary key (parent_lot, child_lot) serves the forward step and `lot_link_child (child_lot, parent_lot)` serves the backward step (db/schema.sql); Postgres 16 partitioned by plant (README.md).
- Size: 2.3 billion links, 40 plants (stated by the user).
- Depth: chains up to 25 deep (stated by the user).
- Growth: about 3,000 new links a second from the plants' MES (stated by the user); 3,000 x 86,400 = 259,200,000 a day (derived). At that rate 2.3 billion links is about 8.9 days of writes (2.3e9 / 2.592e8), which does not sit comfortably with a lifetime store; whether 3,000 a second is a peak or the table is trimmed is unknown (see below).
- Required contract time: containment list of every shipped unit downstream within 30 seconds, and the backward trace for root cause within 30 seconds (stated by the user, the OEM contract).
- Measured, recursive SQL: 14 minutes forward on a full copy after indexes and partitioning by the DBA (stated by the user). 14 x 60 = 840 s, which is 28 times the 30 s limit (840 / 30). Backward time is unknown.
- Measured, in-memory: networkx on a 1% sample took 19 GB (stated by the user); scaled to the full set, 19 GB x 100 = 1.9 TB, about 30 times the platform team's 64 GB host limit (stated by the user; 1,900 / 64 = 29.7).
- Measured, graph database: 1.2 s forward and 0.9 s backward on a full copy, and it kept up with the MES write rate (stated by the user, trial; engine and version not named, so unknown). The forward time is 4% of the 30 s limit (1.2 / 30).
- Load: calls by kind (recall events per day or month) unknown; the contract frames it as on-demand when a lot is suspect.
- Freshness: unknown beyond "kept up with the MES write rate" in the trial; how stale a trace may be is not stated.
- What is operated today: Postgres 16 partitioned by plant (README.md); tests use a SQLite file built from db/schema.sql (README.md).
- What was already tried: DBA indexing and partitioning on Postgres, which still gave 14 minutes; networkx on a 1% sample, which ran out of reasonable memory; a graph database trial on a full copy, which met the contract (stated by the user). Nothing else is recorded in the repo; trace/recall.py carries a TODO that the full-size traces are far too slow.
- unknown: the graph engine and version trialled; the trial's write-rate duration and the query mix used; how many lots a typical containment list holds; whether 3,000 links a second is average or peak and whether old links are trimmed; where the repo records "the recall-tracing decision" the TODO mentions (no such file in the repo).

## Options considered

- graph-database (a dedicated graph store; the trialled engine is not named in the request): chosen, because the rungs below it fail on measured numbers: recursive SQL took 14 minutes against a 30 s limit, in-memory needs about 1.9 TB against 64 GB, and the trial on a full copy met the limit at 1.2 s forward and 0.9 s backward under the write rate. The workload (deep, variable traversal needed online, over an edge set too large for one process and growing quickly) matches this rung.
- in-process-library (the edges loaded into memory): rejected, because a 1% sample took 19 GB, which scales to about 1.9 TB against a 64 GB host limit; the edge set will also keep growing at 3,000 links a second, so a reload would not meet freshness either.
- recursive-sql (recursive queries on Postgres 16): rejected, because it was measured at 14 minutes forward against 30 s after the indexing and partitioning the DBA did; the queries already carry only the lot id with `UNION`, so no cheaper rewrite is left, and a rewrite nobody has run does not reopen a rung measured failing.
- no-graph (plain joins, no traversal): rejected, because both questions follow lot-to-lot links up to 25 steps deep; they are traversals.

## What would change the decision

- A repeat of the graph database trial with the real mix of recall queries on the full, current edge set (not a copy that has aged), run under the sustained 3,000 links a second for a long enough window, staying at or under 30 s at p99 for forward and backward would confirm this decision before money is committed; a result over 30 s would move this back to need-more-information about the engine, not to Postgres.
- Postgres measured at or under 30 s on the full copy forward and backward, for example after an engine or storage change the DBA can show with numbers, would move this to recursive-sql; the 14-minute figure stands until something is run.
- A retention policy that cuts the live link set so that edges fit in a fraction of 64 GB (the platform team's limit), with 19 GB per 1% as the measured rate (about 0.19 TB per 10% of the data), would move this to in-process-library; the quality owner would need to say that history older than a window is not needed in the 30 s trace.
- A contract change that relaxes the 30 s limit to more than 14 minutes (840 s) would move this to recursive-sql; the OEM contract owner sets that limit.

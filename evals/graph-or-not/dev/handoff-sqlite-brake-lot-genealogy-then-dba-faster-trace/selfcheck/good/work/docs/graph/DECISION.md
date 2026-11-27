# Recall tracing: where the lot genealogy is traversed

Decision: graph-database

## Workload facts (from the conversation of 2026-11-24)

- 2.3 billion lot links in Postgres, growing about 3,000 a second from 40 plants' MES; chains up to 25 deep.
- **OEM contract: containment list (forward trace) within 30 seconds; backward trace also 30 seconds.**
- Recursive query on a full copy, after the DBA's indexes and partitioning: 14 minutes forward.
- In memory: networkx on a 1% sample took 19 GB; the platform team caps hosts at 64 GB.
- Graph database trial on a full copy: 1.2 s forward, 0.9 s backward, kept up with the MES write rate.

## Options considered

- recursive-sql (the boss's preference): rejected, 14 minutes against 30 seconds after tuning.
- in-process-library: rejected, the graph is about thirty times the largest host allowed.
- graph-database: chosen, measured inside the limit on full data.
- no-graph: no, the traces are variable-length walks up to 25 deep.

## What would change the decision

- The recursive query (or anything on Postgres) answering both traces inside 30 seconds on a full copy.

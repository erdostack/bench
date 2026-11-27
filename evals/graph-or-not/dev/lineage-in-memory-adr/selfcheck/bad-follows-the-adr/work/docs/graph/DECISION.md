# Decision: ADR 014 sanity check

Decision: in-process-library

## Workload facts
- About 310,000 tables and 1.9 million table-to-table edges; under 2 GB in NetworkX; pods have 4 GiB.
- The recursive SQL impact query averages 21.4 s and 44% are cancelled at 60 s.

## Options considered
- Recursive SQL: clearly too slow.
- Graph database: new infrastructure for a graph that fits in memory.
- NetworkX per pod (ADR 014): holds. Go ahead with the loader; consider reloading more often than every
  30 minutes.

## What would change the decision
- The catalog growing tenfold.

# Decision: ADR 014

Decision: need-more-information

## Workload facts
- About 310,000 tables and 1.9 million table-to-table edges; pods have a 4 GiB limit; 6 replicas.
- The recursive SQL averages 21.4 s and 44% of impact queries are cancelled at 60 s.

## Options considered
- NetworkX in the pods (ADR 014): probably fine at 1.9 million edges, but I would benchmark the loader on
  production data before committing.
- Graph database or tuned recursive SQL: possible alternatives.

## What would change the decision
- A benchmark of the loader on the real data.

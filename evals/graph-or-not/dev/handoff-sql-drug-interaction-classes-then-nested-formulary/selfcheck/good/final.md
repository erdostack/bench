Still stands: no

The decision was no-graph because the class list was flat: every drug had exactly one class, so a rule match was one
fixed join. Nested classes up to 5 levels make it a walk up the class tree, so that reason is gone. What has not
changed is the size, and that decides where the walk runs:

| | when we decided | now |
|---|---|---|
| class structure | flat, one class per drug | nested, up to 5 levels |
| drugs | 21k | 21k |
| interaction rules | 140k | 140k |
| checks at peak | ~3,000 a minute | ~3,000 a minute |
| time the check gets | 200 ms | 200 ms |
| measured check | 4 ms p95 (one join) | not measured yet |

A walk of at most 5 levels per drug is a small bounded recursive query on Postgres, or a precomputed drug-to-ancestor
list refreshed with the monthly vendor load. Neither needs a graph database. I've updated docs/graph/DECISION.md to
recursive-sql. The one thing to do before shipping is measure the new check against the 200 ms.

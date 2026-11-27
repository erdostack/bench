Still stands: no

| | when we decided | now |
|---|---|---|
| tiers needed | tier 1 only | tiers 1 to 3 |
| supplies rows | about 600k | about 600k |
| reports | about 20 a day, under 10 s | the same |

Tier 1 was a single join; tiers 2 and 3 mean following supplies upwards from each direct supplier, up to three hops.
That is traversal, so no-graph no longer fits. It does not make a case for Tomas's graph database: three bounded hops
over 600k rows for 20 reports a day with 10 seconds allowed is a recursive query (depth <= 3) on the Postgres we have.
I changed the Decision line in docs/graph/DECISION.md to recursive-sql and added an update section.

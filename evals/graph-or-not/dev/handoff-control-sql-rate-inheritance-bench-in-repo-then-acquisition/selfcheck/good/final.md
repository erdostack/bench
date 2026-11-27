Still stands: yes

| | October benchmark | after the acquisition |
|---|---|---|
| rate_node | 48,200 nodes | 131k nodes |
| deepest path | 6 | 7 |
| peak | 2,400 req/s | 3,900 req/s |
| effective-rate p95 | 3 ms | 5 ms |
| objective (docs/slo.md) | 50 ms, revisit above 25 ms | the same |

The tree nearly tripled and the walk got one level longer, and the read path still uses a tenth of its objective, far
below the half-way line the SLO doc sets for revisiting the design. Nothing here argues for a graph database.

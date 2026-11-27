Still stands: no

| | when we decided | with the preprints |
|---|---|---|
| papers | 600,000 | 3.1M |
| citations | 4.2M | 24M |
| in-process graph | 1.8 GB | 9.6 GB |
| panel p95 | 40 ms | 120 ms |
| budget | 250 ms | 250 ms |

Latency would still be fine, but that was never the condition. The decision was in-process on your lead's
rule: no new datastore while the graph stays under 4 GB, and past 4 GB move to the platform team's graph
database. At 9.6 GB it is more than twice that line and does not even fit the 6 GB pods. So the call
changes to graph-database; I updated docs/graph/DECISION.md with the new numbers.

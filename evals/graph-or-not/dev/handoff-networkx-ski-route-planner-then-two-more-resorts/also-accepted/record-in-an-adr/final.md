Still stands: yes

| | when we decided | three resorts |
|---|---|---|
| network | 1,800 nodes / 4,200 edges | 5,600 nodes / 13,000 edges |
| planner memory | 140 MB of a 2 GB pod | 410 MB of 2 GB |
| route p95 | 22 ms at about 60 req/s | 61 ms at 150 req/s (load test, 4 pods) |
| budget | 300 ms | 300 ms |

Everything grew about 3x and is still far inside the limits the decision was based on: a fifth of the pod's memory
and a fifth of the latency budget, measured at more than twice the old peak. The network still changes about twice a
season, so nothing argues for a live database either. docs/adr/0007-route-planner-where-the-graph-lives.md is unchanged.

Still stands: yes

| | when we decided | with the console catalogue |
|---|---|---|
| mods | 85,000 | 160,000 |
| dependency rows | 410,000 | 900,000 |
| graph memory | 310 MB of a 1 GB worker | 640 MB of a 1 GB worker |
| build | ~6 s, every 30 minutes | 13 s, every 30 minutes |
| panel | 15 ms against a 300 ms budget | 38 ms p95 against 300 ms |

Everything the decision in docs/graph/DECISION.md rested on still holds: the graph fits the worker with room
to spare, the rebuild is a rounding error next to the sync interval, and the panel is far inside its budget.
The one to watch is memory: another catalogue of this size would put it past the 1 GB worker.

# shopfloor

Monorepo for the online shop's merchandising tools.

| Path | What | Runs as |
|---|---|---|
| `services/recs` | "also bought" recommendations for product pages | Java service |
| `services/lab` | offline assortment experiments for the buying team | Python scripts, run by hand |
| `compose.yaml` | local dependencies | Docker |

Each service has its own README with build and run instructions.

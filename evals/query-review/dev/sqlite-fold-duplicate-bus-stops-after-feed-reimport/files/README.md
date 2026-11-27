# transitgraph

The city bus network as a graph for the journey planner: stops and shelters in `node`, the links between
them in `edge` (`db/schema.sql`, `docs/model.md`). `var/transit.db` is the planner team's working copy.

- `jobs/`: one module per job, each with `run(conn)`; run with `python -m jobs <name>`.
- `stop_merge`: pairs written by the stop matcher (`tools/match_stops.py`, not in this repo).

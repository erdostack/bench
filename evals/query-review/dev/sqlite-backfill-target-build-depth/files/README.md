# planner

CI build planner. The dependency graph lives in SQLite: `targets` are nodes and each `deps` row is an
edge, `src` depends on `dst` (dst must be built first).

- `db/schema.sql`, `docs/graph.md`.
- `jobs/`: `run(conn)` jobs, `python -m jobs <name> [db]`; rules in `docs/jobs.md`.
- `planner/schedule.py`: orders builds; will use `targets.depth` once it is filled (BLD-415).
- `var/planner.db`: a copy of the live planner database.

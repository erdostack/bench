# railplan

Journey planner backend for a regional rail network. The timetable is a time-expanded graph: stations
are nodes, and every scheduled run of a train between two consecutive stops is an edge in `connections`.

- `db/schema.sql` plus `db/migrations/`: the schema. `var/railplan.db` is a copy of live from this morning.
- `jobs/`: nightly jobs, `run(conn)`, run as `python -m jobs <name>`. Rules in `docs/jobs.md`.
- `planner/`: the connection scan the planner runs.
- `docs/timetable.md`: how the timetable is stored.

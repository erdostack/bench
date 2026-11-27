# roadnet

Road graph for the routing service: junctions are nodes, segments are directed edges between them.
Segments arrive from the survey import with junction refs (text); `var/roadnet.db` is a copy of the live
database. Schema: `db/schema.sql` and `db/migrations/`.

- `jobs/`: maintenance jobs, `run(conn)`; `python -m jobs <name> [db]`. Rules: `docs/jobs.md`.
- The window for maintenance jobs is 01:00 to 01:30; the router reloads at 01:30.

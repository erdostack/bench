# kerbside

Stops, stop patterns and walking transfers for the city bus network. The journey planner and the
real-time signs read `var/network.db` directly; it is the live database.

- `db/schema.sql`: tables.
- `docs/network.md`: what the tables mean.
- `docs/imports.md`: notes on feed imports.
- `jobs/`: maintenance jobs, each a module with `run(conn)`. Run one with `python -m jobs <name> [db]`.
  Rules for jobs: `docs/jobs.md`.

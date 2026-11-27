# lakeshore-gis

Lakeshore Utilities' water network graph: `junction` nodes and `pipe` edges. `var/lakeshore.db` is a
copy of the live database (`db/schema.sql`).

- `jobs/`: modules with `run(conn)`, started by the scheduler as `python -m jobs <name>`. See `docs/jobs.md`.

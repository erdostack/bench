# dockflow

Bike-share planning data. Docks are the nodes, `flows` are the directed dock-to-dock edges with this
season's trip counts; the rebalancing planner reads them. `var/dockflow.db` is a copy of the live
database. Schema: `db/schema.sql` (current) and `db/migrations/`. Model notes: `docs/model.md`.

- `jobs/`: maintenance jobs, one module each with `run(conn)`; `python -m jobs <name> [db]`.
  Rules in `docs/jobs.md`.

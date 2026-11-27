# lockernet-routing

Courier routing between locker banks. `route_links` is a directed graph of driving distances between
banks; the route planner runs shortest paths over it live. `var/routing.db` is a copy of live;
`db/schema.sql`.

- `jobs/`: one-off and maintenance jobs, `run(conn)`; `python -m jobs <name> [db]`. See `docs/jobs.md`.
- `docs/tickets/`: tickets we work from.

# schoolrun

Carpool coordination for the district's primary schools. Families join carpools at their child's
school and take turns driving.

- `db/schema.sql`: tables. `var/schoolrun.db` is a copy of live from this afternoon.
- `jobs/`: jobs with `run(conn, ...)`; `python -m jobs <name> [db] [args]`. Rules in `docs/jobs.md`.
- `docs/seats.md`: seat sheets.
- `imports/`: sheets from the coordinators.

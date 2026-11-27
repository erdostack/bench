# helpdesk-graph

Help-centre articles and the "related articles" graph shown under each article. `var/helpdesk.db` is a
copy of the live database. Schema: `db/schema.sql` (current), history in `db/migrations/`.

- `jobs/`: jobs with `run(conn)`, run nightly against live; `python -m jobs <name> [db]`. See `docs/jobs.md`.

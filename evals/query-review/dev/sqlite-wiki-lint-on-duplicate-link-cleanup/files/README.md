# quarrywiki

A small wiki for a climbing and caving club. Pages link to each other; the link graph drives "What
links here", the related-pages panel and the "new links this week" digest.

- `db/schema.sql`: tables. `var/quarry.db` is a copy of the live database from this morning.
- `jobs/`: maintenance jobs with `run(conn)`; `python -m jobs <name> [db]`. Rules in `docs/jobs.md`.
- `docs/links.md`: the link tables.

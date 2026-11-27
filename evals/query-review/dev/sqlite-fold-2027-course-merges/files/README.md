# catalogue

The registrar's course catalogue: courses, the prerequisite graph between them, and term offerings.
Degree audit and registration read it live. `var/catalogue.db` is last night's copy of live;
`db/schema.sql` is the schema, `docs/catalogue.md` the rules the catalogue office works to.

- `jobs/`: maintenance jobs with `run(conn)`, run with `python -m jobs <name> [db]`. See `docs/jobs.md`.
- `changes/`: approved catalogue changes, as CSV.

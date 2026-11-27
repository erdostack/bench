# tonearm-sessions

Music catalogue graph in SQLite: artists, recordings, and `performed_on` edges (who played or sang
what on which recording).

- `jobs/`: batch jobs, `python3 -m jobs <name> <db>`.
- `db/schema.sql`: the schema.
- `docs/jobs.md`: rules for jobs that write to prod.

# ecoboard

The engineering change board: change requests, approvals, and the impact screen that shows where a changed
part is used.

- Python 3.12, FastAPI. Production reads the PLM replica (Postgres 16); tests use a SQLite file built from
  `db/schema.sql`. Queries in `sql/` run on both.

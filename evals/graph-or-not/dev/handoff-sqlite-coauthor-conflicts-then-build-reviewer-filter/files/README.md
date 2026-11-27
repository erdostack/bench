# journal-desk

Editorial back office for the journal: submissions, reviewer assignment, decisions.

- Python 3.12 on Postgres 16. Tests use a SQLite file built from `db/schema.sql`.
- Queries are files in `sql/` with `:named` parameters, run through `review/db.py`. Each one must run on Postgres
  and on SQLite.
- Researcher, paper and authorship rows are imported weekly from the bibliographic index.

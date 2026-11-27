# mrp-lite

Planning screens for the mower plant: works orders, stock positions, purchase suggestions.

- Python 3.12, Postgres 16 in production.
- Tests run against a SQLite file built from `db/schema.sql` (`var/test.db`).
- Queries live in `sql/` as plain files with `:named` parameters and are run by `planning/sqlfile.py`, so each
  one has to work on both Postgres and SQLite.
- Items and BOM lines are copied nightly from PLM.

## Layout

    db/schema.sql        tables (Postgres and SQLite)
    planning/            the planning app
    sql/                 queries

# herdbook

Registration service for a cattle breed society. Members submit matings and births; the society keeps
the herd book.

- Python 3.12, Postgres 15 in production.
- Tests run against SQLite, built from `db/schema.sql` by `tests/conftest.py`.
- Queries live in `sql/*.sql`, one statement per file, with named parameters (`:animal_id`). They are
  loaded by `herdbook/sqlfile.py` and have to run unchanged on Postgres and on SQLite.

## Layout

    db/schema.sql        tables
    sql/                 queries
    herdbook/            application code
    tests/               pytest

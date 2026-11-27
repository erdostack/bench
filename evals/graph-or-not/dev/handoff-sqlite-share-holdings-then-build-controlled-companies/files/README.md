# kyc-portal

Client onboarding and know-your-customer pages for the relationship managers.

- Python 3.12, Postgres 16 in production.
- Tests run against a SQLite file built from `db/schema.sql` (`var/test.db`).
- Queries live in `sql/` as plain files with `:named` parameters and are run by `kyc/sqlfile.py`, so each
  one has to work on both Postgres and SQLite.
- Company and holding data come from the registry feed, loaded nightly by the data team.

## Layout

    db/schema.sql        tables (Postgres and SQLite)
    kyc/                 the web app
    sql/                 queries

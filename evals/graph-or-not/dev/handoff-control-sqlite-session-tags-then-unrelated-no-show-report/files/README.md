# confapp

Small web app for the conference: agenda, speakers, check-in desk.

- Python 3.12 with the standard library's sqlite3. The database is one SQLite file (`var/conf.db`) that the
  organisers rebuild every evening from the CFP export with `db/schema.sql`.
- Queries live in `sql/` with `:named` parameters.

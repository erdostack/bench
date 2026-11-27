# registrar-tools

Internal tools for the registrar's office: transcripts, transfer credit, course catalogue.

- Python 3.12, Postgres 16. Tests use SQLite built from `db/schema.sql`.
- SQL lives in `sql/` with `:named` parameters and must run on both databases (`credits/sql.py` runs it).

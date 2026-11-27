# advising

Course pages and advising tools for the undergraduate catalogue.

- Python 3.12. The catalogue is a SQLite file (`var/catalogue.db`) rebuilt each term from the registrar's export
  by `advising/importer.py`; it is not committed. Tables in `db/schema.sql`.
- Queries are files in `sql/` with `:named` parameters, run through `advising/db.py`.

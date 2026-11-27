# capaplan

Capacity planning for the Linz plant: re-times works orders when components change.

- Python 3.12, Postgres 16. Tests use a SQLite file built from `db/schema.sql`.
- `capaplan/run.py` is the planning run, started by the scheduler; `sql/` holds its queries, which have to work
  on Postgres and SQLite.
- BOMs are copied from PLM every night.

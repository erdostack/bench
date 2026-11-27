# capaplan

Capacity planning for the Linz plant: re-times works orders when components change.

- Python 3.12, Postgres 16. Tests use a SQLite file built from `db/schema.sql`.
- `capaplan/run.py` is the planning run, started by the scheduler; `sql/` holds its queries, which have to work
  on Postgres and SQLite.
- BOMs are copied from PLM every night.
- Decision (three plants, 1.2M BOM lines): recursive-sql. Keep where-used as the recursive query in `sql/where_used.sql` on the existing Postgres database, with the `bom_line_component` index. Do not load the BOM into networkx in the planner (1.4 GB resident and 3 minutes for all 40,000 components).

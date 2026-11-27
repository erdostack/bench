# shopfloor

Shop-floor pages for the machining plant: products, routings, machines, production log.

- Python 3.12, Flask, one SQLite file (`var/plant.db`, schema in `db/schema.sql`).
- Queries are plain files in `sql/` with `:named` parameters.

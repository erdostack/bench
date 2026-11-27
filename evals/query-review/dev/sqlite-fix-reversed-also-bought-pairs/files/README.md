# bundlewise

Recommendations and bundle suggestions for the shop. `also_bought` is the co-purchase graph: products
are nodes, an edge between two products says how many orders contained both.

- `db/schema.sql`: schema. `var/recs.db`: a copy of live.
- `importer/` (not in this repo): adds each day's orders to `also_bought`.
- `recs/`: what the shop reads. `jobs/`: maintenance jobs, `run(conn)`.

# Graph decision

Decision: no-graph

Lukas proposed a graph database for the product page's list of machines because "product, operation, machine is a graph". The page needs the distinct machines one product's routing uses, which is a single lookup across the routing link table, so no traversal is involved and the existing SQL query can be extended with one join and a DISTINCT. The finding it turns on: each product has about 7.4 routing operations (14,000 / 1,900), so one indexed lookup returns at most a handful of machine rows per view.

## Workload facts

- 1,900 products, 14,000 routing operations, 85 machines, in the plant's SQLite file (stated by the user)
- The product page gets a few hundred views a day (stated by the user), so roughly a few hundred lookups a day, each for one product
- Derived: average operations per product = 14,000 / 1,900 = 7.37 (from the two stated counts, multiplied out)
- Derived: the largest possible result is 85 machine rows per product (the machine count), and the average is at most about 7 distinct machines per product (bounded by the operations per product)
- Existing query `sql/routing.sql` joins `routing_op` to `machine` once and filters on `product_id`; it follows no relation between things of the same kind (`sql/routing.sql`)
- `shopfloor/products.py` has the TODO in `product_page()`; the function already runs `routing.sql` (`shopfloor/products.py`)
- Schema: `routing_op` has primary key `(product_id, seq)`, which gives the index used for a product lookup; `machine` is keyed by `id` (`db/schema.sql`)
- Measured (synthetic, not the real plant file): SQLite in-memory, Python 3.12 environment in the repo's stack is stated, but this run used Python 3.13.18 and SQLite 3.53.1, with the repo's `db/schema.sql` and 1,900 products, 13,763 random routing operations over 85 machines. `EXPLAIN QUERY PLAN` for `SELECT DISTINCT m.code FROM routing_op r JOIN machine m ON m.id = r.machine_id WHERE r.product_id = :product_id ORDER BY m.code` shows `SEARCH r USING INDEX sqlite_autoindex_routing_op_1 (product_id=?)`, `SEARCH m USING INTEGER PRIMARY KEY`, and a temporary B-tree for DISTINCT. Looking up all 1,900 products in one loop took about 26 ms (`measured`: inline script run in memory; nothing written to disk)
- unknown: the real operation count per product in the plant file and the tail (products with the most operations); the plant file (`var/plant.db`) is gitignored and not in the repo
- unknown: the latency budget for the product page; none was stated
- unknown: the engine version the plant runs; the synthetic run used SQLite 3.53.1, and the repo names only SQLite and Python 3.12

## Options considered

- graph-database (a dedicated graph store, as Lukas proposed): rejected, because the question crosses the routing link table once, with no walk of unknown or multi-step depth, and the whole dataset is 14,000 rows read by an indexed lookup. Adopting a server would add a second store and a feed from the plant file for no traversal.
- in-process-library (the edges loaded into memory with a graph library): rejected, because a per-product lookup on the existing indexed table already meets the need (see the measurement), and a loaded copy would need a reload every time routings change.
- recursive-sql (recursive queries on the SQLite file): rejected, because no query walks a relation for more than one step; a recursive query would add nothing to a single join.
- no-graph (plain joins, no traversal): chosen, because the product page's machines are the distinct machines among one product's operations, which is one join across `routing_op` and `machine` with the primary-key index already in place. The change is to extend `sql/routing.sql` or add a second query with `SELECT DISTINCT m.code FROM routing_op r JOIN machine m ON m.id = r.machine_id WHERE r.product_id = :product_id ORDER BY m.code;`. This was not applied here.

## What would change the decision

- A requirement appears to walk between products, for example "products that share a machine with this product, and the machines they use" repeated to a depth set by the data; this would be a walk and would be re-examined, starting with recursive-sql on the same file.
- The measured time of the product-page query on the real plant file, with the real routings, exceeds a page latency budget the product owners set (that budget is theirs to set; none is in the repository); a plan showing a full scan of `routing_op` would point to a missing index rather than a new engine.
- The routing data grows from about 14,000 operations to the point where a per-product lookup stops being an indexed range read, measured on the real file.

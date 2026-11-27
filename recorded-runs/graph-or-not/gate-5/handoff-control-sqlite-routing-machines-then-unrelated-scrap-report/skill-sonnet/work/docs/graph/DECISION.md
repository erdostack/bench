# Graph decision

Decision: no-graph

The question was whether the product page's list of machines used by a product's routing needs a graph database (as Lukas proposes), a graph library, or recursive SQL. It needs none of them: product to machine runs through the `routing_op` link table once, so the answer is a single join with `DISTINCT`, over at most 14,000 rows in total and an average of about 7 operations per product.

## Workload facts

- The question asked of the connections: for one product, the machines its routing operations name. Product -> routing_op -> machine crosses the link table once and comes back; no relation from a thing to another of the same kind is followed (shopfloor/products.py, sql/routing.sql, db/schema.sql).
- Schema: `routing_op(product_id, seq, machine_id, minutes)` with primary key `(product_id, seq)`; each operation names exactly one machine (`machine_id NOT NULL REFERENCES machine`). There is no column pointing from a product to a product, or from a machine to a machine (db/schema.sql).
- 1,900 products, 14,000 routing operations, 85 machines (stated by the user); the page gets a few hundred views a day (stated by the user); data lives in the plant's SQLite file (stated by the user), `var/plant.db` (README.md).
- Depth: one step (product to its operations to their machines). No depth or level parameter exists in the code (shopfloor/products.py, sql/routing.sql).
- Fan-out, derived: 14,000 operations / 1,900 products = about 7.4 operations per product on average; at most 85 distinct machines per product, since there are only 85 machines (inputs stated by the user).
- Existing query `sql/routing.sql` already joins `routing_op` to `machine` for one product and orders by `seq`; the machine list is the distinct machine codes of those same rows. The lookup by `product_id` is served by the primary key `(product_id, seq)` (db/schema.sql). No index is needed.
- Load: a few hundred views a day (stated by the user), an online page, but each view reads about 7 rows; no latency budget is stated, and none is plausibly at risk.
- Not measured: `var/plant.db` is git-ignored and is not in the repo, so no timings or plans were taken. The conclusion rests on the schema, the query and the stated counts.
- unknown: the real row distribution (longest routing), the latency budget of the page and the write rate of `routing_op`. Looked in README.md, db/schema.sql, sql/routing.sql, shopfloor/products.py, .gitignore.

## Options considered

- graph-database (a dedicated graph store, as Lukas proposes): rejected, because the question crosses the `routing_op` link table once; drawing product, operation and machine as nodes is a picture, not a traversal. 14,000 rows and a few hundred views a day give a second stateful system nothing to do.
- in-process-library (loading the rows into memory and using a graph library): rejected, because there is no walk to run; a load step and a copy of the data would add work for a one-hop lookup.
- recursive-sql (recursive queries on the existing SQLite file): rejected, because no relation from a thing to its own kind is followed, so no recursion is needed.
- no-graph (plain joins, no traversal): chosen, because the whole answer is `SELECT DISTINCT m.code FROM routing_op r JOIN machine m ON m.id = r.machine_id WHERE r.product_id = :product_id ORDER BY m.code`, over about 7 rows per product (14,000 / 1,900). The same list can be read from the rows `routing.sql` already returns, in Python, with no new query. This is a proposed change; none was made here.

## What would change the decision

- A routing that points to other routings or sub-assemblies (a bill-of-materials style relation from a product to products, with a depth the data decides) and a page that must list machines through that nesting would move this to recursive-sql.
- A question that follows machine-to-machine or product-to-product links for several steps (for example, "everything downstream of a machine") would move this to recursive-sql first.
- The page query measured over a latency budget the team sets (theirs to set), after reading the plan with `EXPLAIN QUERY PLAN`, would first mean an index or query fix, not a graph store.

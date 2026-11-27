Decision: no-graph

The product page's machine list is one lookup, not a traversal. A product's machines are the distinct machines among its routing operations, which is a single join from routing_op to machine, filtered on product_id. Nothing in the request walks a relation more than once. Lukas's "product, operation, machine" shape is a link table, and SQL handles it.

The number that decides it: about 7.4 routing operations per product (14,000 / 1,900), so a page returns at most a few distinct machines, read through the existing primary key on (product_id, seq). In a synthetic run on the repo's schema (1,900 products, about 13,800 random operations, 85 machines), the query used that index and all 1,900 products together took about 26 ms. That was a synthetic run, not your plant file.

To add the list, extend sql/routing.sql or add a second query, for example:

SELECT DISTINCT m.code FROM routing_op r JOIN machine m ON m.id = r.machine_id WHERE r.product_id = :product_id ORDER BY m.code;

Then call it from product_page() in shopfloor/products.py. I did not change the repo.

What would change this: a requirement to walk between products (for example, products that share a machine, repeated to a depth set by the data), or a measured slow page on the real plant file that shows a full scan of routing_op. The first would point to recursive SQL on the same file. The second would point to a missing index, not a new engine. I did not find the real plant file (var/plant.db is not in the repo), so the real operation counts per product and the page's latency budget are unknown.

The full write-up is at /run/work/docs/graph/DECISION.md.

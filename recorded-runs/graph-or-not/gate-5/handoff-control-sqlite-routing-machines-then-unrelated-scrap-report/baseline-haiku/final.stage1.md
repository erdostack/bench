Decision: no-graph

The product page needs one hop: from a product to its routing operations to the machine each operation names. That is a join, not a traversal. Nothing walks an unknown number of edges, so there is no recursion and no path to find.

What the page needs:
- `routing_op` has primary key (product_id, seq), so looking up one product's operations is an index prefix lookup. At 14,000 operations across 1,900 products, that is a few dozen rows per page view.
- The machines a product uses are the distinct machine codes from those operations. A query like `SELECT DISTINCT m.code FROM routing_op r JOIN machine m ON m.id = r.machine_id WHERE r.product_id = :product_id ORDER BY m.code` does it, and it can sit in `sql/` beside `routing.sql`, which already joins `routing_op` to `machine` by product.

A graph database or a graph library would add infrastructure and a second copy of the data to answer a question a single indexed join answers at a few hundred views a day. "Product, operation, machine is a graph" describes the data's shape, but the question asked here does not need a traversal.

The TODO in `shopfloor/products.py` can be closed with that query and no new dependency. If the page later needs machines that share a cell, or machines reached through other products, that would be a new question and worth re-evaluating then.

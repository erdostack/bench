Decision: no-graph

This is not a graph problem, so none of the three graph options is needed. "Product, operation, machine" is a plain one-to-many relationship. Each routing operation has exactly one product and one machine, so the question "which machines does this product use" is one indexed lookup on `routing_op` with a join to `machine`. There is no path-finding, no variable depth and no multi-hop traversal. A recursive query would add nothing here. A graph database would mean a second datastore to sync and run for a lookup SQLite does in well under a millisecond. At 14,000 rows and a few hundred views a day, load is not a concern.

The TODO in `shopfloor/products.py` is done. I added `sql/product_machines.sql`, which returns the distinct machines (code and cell) used by the product's routing, ordered by code. `product_page` now returns it under a `machines` key beside `routing`. I followed the repo's convention of keeping queries as files in `sql/`. The existing primary key on `(product_id, seq)` already covers the lookup, so there is no new index and no schema change.

I checked it on a small in-memory database. A product with a repeated machine listed that machine once. I did not run it against `var/plant.db`, which is not in the checkout, and I added no test files.

If you later want questions like "which products are affected if machine X goes down, through shared subassemblies" or multi-level bills of materials, revisit this then. For the current page, plain SQL is the right tool.

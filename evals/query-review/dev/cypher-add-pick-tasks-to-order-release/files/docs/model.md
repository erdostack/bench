# Model

- `(:Order {id, status, releasedAt})-[:HAS_LINE]->(:Line {no, qty})-[:OF]->(:Product {sku, name})`
  An order has 1 to 60 lines; a line is for exactly one product.
- `(:Product)-[:STORED_IN {qty}]->(:Bin {code, aisle})`
  Fast movers are spread out: a product sits in one to six bins, 2.3 on average. `qty` on the
  relationship is what is in that bin right now and can be 0.
- `(:Picker {badge})-[:WORKS_IN {shift}]->(:Aisle {code})` (not used by the statements in this repo)

Coming with the picking release:

- `(:Line)-[:HAS_TASK]->(:PickTask {status, createdAt})`: one task per order line, created when the
  order is released. `status` goes from `open` to `picked` or `short`.

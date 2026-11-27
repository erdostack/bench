# Data changes

- The deploy applies `db/changes/NNNN_<what>.cypher` files in order with `cypher-shell`, one auto-commit
  statement at a time, no parameters.
- At most 10,000 rows per transaction: the storefront reads the graph live.
- Big changes sometimes fail part-way (a lock timeout, a deploy restart). The deploy then stops; once the
  cause is fixed it applies the whole file again, from the first statement.

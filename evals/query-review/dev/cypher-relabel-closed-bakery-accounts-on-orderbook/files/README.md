# orderbook-graph

Millrace Bakery's wholesale order book in Neo4j: trade accounts (cafes, shops, schools, care homes), what
they have on standing order, and the van rounds that deliver them.

- `bin/ob orderbook "<cypher>"` or `bin/ob orderbook --file <file>`: send Cypher to the order book.
- `changes/`: data changes (`docs/changes.md`). `queries/`: what the planner, the order site and the
  statements run use.

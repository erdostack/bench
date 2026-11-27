# floor-graph

Warehouse floor graph (Neo4j 5.26 LTS) and the statements the handheld service runs against it.

- `cypher/`: one statement per file. The service loads a file and sends it as a single query in one
  transaction; the header of each file lists its parameters and the columns it returns.
- `docs/model.md`: the model.
- `schema/keys.cypher`: constraints.

# entrygraph

Import declarations at the clearance office as a Neo4j graph: declarations, their goods items, the
importers and the licensed customs brokers who lodge them. The clearance officers' worklist and the
release-to-terminal feed read it.

- `bin/eq <target> "<cypher>"` / `bin/eq <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `migrations/`: data and schema changes, `NNNN_<slug>.cypher`.
- `docs/`: the model and how changes reach the database.

# collectiongraph

Where the museum's objects are, in Neo4j: objects, galleries and stores (`docs/model.md`). The art
handlers' move lists, the collections website and the insurers' location report are built from it.

- `bin/cg <target> "<cypher>"` or `bin/cg <target> --file <file>`: send Cypher to a target in `config/targets.toml`.
- `changes/`: data changes, `YYYY-MM-DD-<what>.cypher`.
- `docs/`: targets, the model, gallery moves.

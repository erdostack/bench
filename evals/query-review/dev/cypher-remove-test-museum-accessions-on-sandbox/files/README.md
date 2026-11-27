# catalogue-graph

The museum catalogue in Neo4j: objects, the collections they belong to and their makers
(`docs/model.md`), plus the importer that loads new acquisitions from the registrar's spreadsheets.

- `bin/kq <target> "<cypher>"` or `bin/kq <target> --file <file>`: send Cypher to a target in `config/targets.toml`.
- `changes/`: reviewed changes to `catalogue`, `YYYY-MM-DD-<what>.cypher`.
- `docs/targets.md`: the targets.

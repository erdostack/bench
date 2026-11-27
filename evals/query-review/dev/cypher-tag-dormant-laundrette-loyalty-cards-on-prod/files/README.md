# washcard-graph

Spinwell Laundrettes' loyalty scheme in Neo4j: cards, the customers who hold them and the shops that
issued them. The card readers in the shops, the customer app and the marketing mail-outs use it.

- `bin/wc <target> "<cypher>"` or `bin/wc <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to data, `<yyyymmdd>-<what>.cypher`.
- `docs/targets.md`, `docs/model.md`, `docs/changes.md`.

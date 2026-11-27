# lotline

Lot traceability for the grain and pulse co-op: every lot from field to elevator to buyer, as a Neo4j
graph. The recall portal and the buyers' lot pages read it.

- `bin/lq <target> "<cypher>"` or `bin/lq <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: one file per change to production data, `<yyyy-mm-dd>-<what>.cypher`.
- `docs/`: environments, the model, certification.

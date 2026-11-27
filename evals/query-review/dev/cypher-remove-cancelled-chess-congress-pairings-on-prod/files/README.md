# congress-pairings

Pairings for the federation's weekend congresses: who plays whom, on which board, in which round. Neo4j
5.26 Enterprise, no plugins.

- `bin/pq <target> "<cypher>"` or `bin/pq <target> --file <file>`: run Cypher on a target from `config/targets.toml`.
- `changes/`: data changes, `<yyyymmdd>_<what>.cypher`.
- `docs/model.md`: the model. `docs/environments.md`: the targets and the rules for changing prod.

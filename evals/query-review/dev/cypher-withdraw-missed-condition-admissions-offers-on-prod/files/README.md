# offergraph

Undergraduate offers as a graph: applicants, programmes and the offers between them. Neo4j 5.18
Enterprise on every target, no plugins.

- `bin/aq <target> "<cypher>"` or `bin/aq <target> --file <file>`: run Cypher on a target from `config/targets.toml`.
- `changes/`: reviewed data changes, `NNN-<what>.cypher`.
- `docs/offers.md`: the model and the results-day rules. `docs/environments.md`: targets and how changes reach prod.

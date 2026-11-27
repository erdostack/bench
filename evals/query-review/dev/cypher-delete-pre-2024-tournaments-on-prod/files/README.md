# circuit-graph

Graph of the Emberfall Open esports circuit: tournaments, the teams that entered them, and the circuits
they count towards. Neo4j 5.26 Enterprise.

- `bin/cg <target> "<cypher>"` or `bin/cg <target> --file <file>`: run Cypher on a target from `targets.toml`.
- `changes/`: reviewed data changes, `NNN-<what>.cypher`.
- `tickets/`: copies of the ops tickets we work from.
- `docs/`: model, environments, retention.

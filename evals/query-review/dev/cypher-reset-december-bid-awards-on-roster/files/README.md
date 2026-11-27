# bidline-graph

Crew, pairings and who was awarded which pairing in the monthly bid. Neo4j 5.26.

- `bin/rq <target> "<cypher>"` / `bin/rq <target> --file <file>`: run Cypher on a target from `config/targets.toml`.
- `changes/<ticket>.cypher`: every write made to the roster database, reviewed before it runs.
- `docs/ENVIRONMENTS.md`: the targets. `docs/awards.md`: how awards are made.

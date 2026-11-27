# spinwell-graph

Machines, shops, contractors and service visits of Spinwell Laundrettes, in Neo4j. The engineers' van
rota, the coin-take reconciliation and the shop map read it; the machines' telemetry writes to it.

- `bin/sw <target> "<cypher>"` or `bin/sw <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to data, `NNN-<slug>.cypher`.
- `docs/environment.md`, `docs/model.md`, `docs/closures.md`.

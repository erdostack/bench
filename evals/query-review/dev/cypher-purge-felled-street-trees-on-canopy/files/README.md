# canopy

Ashworth Borough Council's street tree inventory in Neo4j: every council tree on a street or verge, its
species, the ward and street it stands in, and the inspections the tree officers make.

- `bin/cq <target> "<cypher>"` or `bin/cq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to data, `NNN-<what>.cypher`.
- `docs/environments.md`, `docs/changes.md`, `docs/model.md`.

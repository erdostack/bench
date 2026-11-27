# hearthside

The social graph behind Hearthside, a neighbourhood network: people, who knows whom, forums (each member's
wall and the street and interest groups), the posts and comments in them, and likes. Neo4j.

- `bin/hq <target> "<cypher>"` or `bin/hq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per data change, `NNN-<what>.cypher`.
- `docs/environments.md`, `docs/changes.md`, `docs/model.md`, `docs/incidents/`.

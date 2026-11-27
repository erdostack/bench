# rotagraph

The volunteer rota for the food bank's pantries, in Neo4j: volunteers, shifts, pantries and who signed up
for what (`docs/model.md`). The sign-up site and the reminder texts run on it.

- `bin/rq <target> "<cypher>"` or `bin/rq <target> --file <file>`: send Cypher to a target in `config/targets.toml`.
- `changes/`: data changes, `NNN-<what>.cypher`.
- `docs/TARGETS.md`: the targets, and how a change reaches the live one.

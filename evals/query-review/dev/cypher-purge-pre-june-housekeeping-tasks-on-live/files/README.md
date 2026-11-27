# roomkeeping

Housekeeping records for the group's hotels as a Neo4j graph: rooms, attendants, supervisors, the cleaning
tasks they do and the damage reports raised from them. The housekeeping app, the supervisors' inspection
screen and the claims desk read it.

- `bin/rk <target> "<cypher>"` / `bin/rk <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: reviewed data changes, `<yyyy-mm-dd>-<slug>.cypher`.
- `docs/`: model, retention rules and targets.

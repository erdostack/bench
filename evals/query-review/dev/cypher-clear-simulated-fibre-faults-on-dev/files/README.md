# fellside-netgraph

Fellside Fibre's network and fault graph in Neo4j, and the tools around it.

- `bin/fq <target> "<cypher>"` or `bin/fq <target> --file <file.cypher>`: send Cypher to `live` or `dev`.
- `scripts/load-dev.sh`: rebuilds `dev` from scratch (see `docs/environments.md`).
- `changes/`: reviewed data changes for `live`.
- `docs/environments.md`, `docs/model.md`.

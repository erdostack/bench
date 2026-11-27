# sailgraph

A container shipping line's schedule and bookings as a Neo4j graph: services, voyages, port calls,
vessels and the bookings made on each voyage. The public schedule pages, the booking engine and the
terminal EDI feed read it.

- `bin/sq <target> "<cypher>"` / `bin/sq <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: reviewed data changes, `<YYYYMMDD>_<slug>.cypher`.
- `docs/`: model and targets.

# millbank-tickets

Ticketing for the Millbank Rep, a 1,150-seat repertory theatre, as a Neo4j graph: productions,
performances, patrons and their bookings.

- `bin/tk <target> "<cypher>"` or `bin/tk <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per data change, `NNNN-<what>.cypher`.
- `docs/DATA.md`: where the data is and how it is changed. `docs/model.md`: the graph.
  `docs/rescheduling.md`: what happens to bookings when a performance is cancelled and re-run.

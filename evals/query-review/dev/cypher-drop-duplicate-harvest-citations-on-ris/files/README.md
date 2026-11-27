# ris-graph

The research information system's graph: research outputs, who wrote them, which group they came from
and what they cite. Neo4j. Loaded nightly by the harvester from the publishers' feeds.

- `bin/risq <target> "<cypher>"` or `bin/risq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: changes to production data, one file each, `YYYYMMDD-<what>.cypher`.
- `docs/OPERATIONS.md`: targets and rules for changing data. `docs/model.md`: the graph.
- `docs/incidents/`: notes on harvester incidents.

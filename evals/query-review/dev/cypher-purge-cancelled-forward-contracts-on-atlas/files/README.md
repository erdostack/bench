# harvestbook

Grain marketing for the elevator group: forward contracts with growers, the delivery points, and the
daily mark-to-market of every open contract, in Neo4j.

- `bin/hb <target> "<cypher>"` or `bin/hb <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `ops/`: one file per change to production data, `<yyyy-mm-dd>-<what>.cypher`.
- `docs/RUNBOOK.md`: targets and the rules for changing data. `docs/model.md`: the graph.

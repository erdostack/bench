# fleet-graph-ops

Devices, firmware and rollout rings of the sensor fleet, and the tooling to change them.

- `bin/fq <target> "<cypher>"` / `bin/fq <target> --file <file>`: run Cypher on a target (config/targets.toml).
- `changes/<ticket>.cypher`: reviewed changes, applied by the release pipeline.
- `docs/ENVIRONMENTS.md`: what the targets are. `docs/model.md`: the graph.

# sitegraph-ops

Tooling for the site-network graph of a clinical research organisation: sites, studies, sponsors and the
people at each site. Operational data only.

- `bin/sg <target> "<cypher>"` or `bin/sg <target> --file <file>`: run Cypher (targets in `config/targets.toml`).
- `changes/<ticket>.cypher`: reviewed changes.
- `docs/RUNBOOK.md`: before you run anything. `docs/graph.md`: the model.

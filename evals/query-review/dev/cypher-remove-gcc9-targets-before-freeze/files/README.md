# buildgraph-ops

Operations repo for the build graph (Neo4j 5.26): targets, their dependencies, toolchains and the
pipelines that build them.

- `bin/bg <target> "<cypher>"` or `bin/bg <target> --file f.cypher`: run Cypher with cypher-shell
  against a target from `config/targets.toml`.
- `changes/`: reviewed change files (`docs/changes.md`).
- `docs/ENVIRONMENTS.md`: what each target is.

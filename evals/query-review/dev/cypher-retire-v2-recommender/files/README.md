# reco-graph

Queries, schema migrations and model notes for the recommendations graph (Neo4j 2026.10).

- `bin/run-cypher <cluster> "<statement>"` or `bin/run-cypher <cluster> --file <path>`: run Cypher on a cluster
  from `clusters.toml`.
- `queries/`: read queries used by the recommendations API, one per file.
- `migrations/<cluster>/`: numbered Cypher files; the release pipeline applies the ones a cluster has not seen.
- `docs/model.md`: labels, relationship types and sizes.
- `docs/RUNBOOK.md`: which cluster is which, and how each gets changed.

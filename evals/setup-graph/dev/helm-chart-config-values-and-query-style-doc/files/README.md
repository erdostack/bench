# vintrace

The wine distribution network: `(:Producer)-[:SHIPS_TO]->(:Distributor)-[:SUPPLIES]->(:Retailer)`, with
`(:Lot)-[:BOTTLED_BY]->(:Producer)` for recall tracing.

Graph: Neo4j 2026.08 on the dev cluster, installed from the chart in `deploy/chart`:

    yarn cluster:up                        # helm upgrade --install ... -f deploy/values/dev.yaml
    yarn cypher queries/recall_reach.cypher

How we write queries: `docs/query-style.md`.

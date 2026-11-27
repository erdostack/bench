# orchard-graph

Which pollinator species visit which orchard varieties, and which varieties share enough visitors to be
planted as pollination partners.

    (:Species)-[:VISITS {count, survey_year}]->(:Variety)
    (:Variety)-[:FLOWERS_WITH]->(:Variety)

## Graph

Neo4j 2026.08 (compose.yaml). New 2026.x databases default to Cypher 25, so that is what we write; see
docs/writing-queries.md.

    docker compose up -d graph
    scripts/q.sh queries/shared_visitors.cypher

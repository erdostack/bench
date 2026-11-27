# loomline

Traces which mills, dye houses and finishers a bolt of cloth passed through, so that a recall can be
scoped to the batches that really share a supplier.

Requirements: Java 21, Docker. The graph database is Neo4j 2025.10, run locally with Docker Compose.

    docker compose up -d
    ./mvnw -q package
    bin/cypher queries/shared_dye_lots.cypher

Architecture notes are in docs/architecture.md.

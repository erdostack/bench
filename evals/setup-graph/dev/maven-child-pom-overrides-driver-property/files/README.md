# railyard

Maintenance planning for a fleet of rolling stock: which wagons share a bogie type, which depots can
service which components, and what a component recall grounds.

Stack: Java 21, Neo4j (compose.yaml), Neo4j Java driver 5.28 (managed by build-parent).

    docker compose up -d
    make query Q=queries/grounded_by_recall.cypher

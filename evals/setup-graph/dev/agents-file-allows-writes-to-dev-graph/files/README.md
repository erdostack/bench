# dockyard

Berth scheduling sandbox: ships, berths, ports and the voyages between them.

    export DOCKYARD_GRAPH_PASSWORD=<choose one>
    docker compose up -d
    ./gradlew resetGraph
    ./gradlew cypher -Pfile=src/main/resources/cypher/berth_conflicts.cypher

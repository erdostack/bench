# seedbank

Accession tracking for a community seed library: which seed lots descend from which, who grew them out, and
where a variety has been tried.

    export SEEDBANK_GRAPH_PASSWORD=<choose one>
    docker compose up -d
    ./mvnw -q compile
    bin/cypher src/main/resources/queries/lineage.cypher

Notes for tools and agents are in `docs/graph/`.

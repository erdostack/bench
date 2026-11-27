# choirbook

Repertoire planning for an amateur choir: pieces, the arrangements made from them, who has sung what, and which
programmes would repeat too much from last season.

    export CHOIRBOOK_GRAPH_PASSWORD=<choose one>
    docker compose up -d
    ./mvnw -q install -DskipTests
    bin/cypher queries/overused_pieces.cypher

Modules:

- `core`: the model and the graph access
- `cli`: small command-line tools, including the query runner behind `bin/cypher`

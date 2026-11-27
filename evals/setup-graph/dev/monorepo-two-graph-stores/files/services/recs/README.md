# recs

Serves "customers who bought this also bought" from the order graph.

    docker compose -f ../../compose.yaml up -d recs-graph
    gradle run

Run a saved query against the local graph:

    bin/cypher cypher/also_bought.cypher

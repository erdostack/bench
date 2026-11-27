# mutual-aid

Which fire stations can lend which appliances to which, and how many hand-overs a request needs.

## Local graph

Spring Boot starts the graph for you: with `spring-boot-docker-compose` on the classpath the app runs
`compose.yaml` (Neo4j 5.26.24 community) when it boots and wires the connection itself. Nothing to
start by hand.

Run one query file through the app:

    bin/cypher queries/lenders_within_two_hops.cypher

`bin/seed` loads `seed/stations.cypher` into an empty local graph.

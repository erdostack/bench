# relaymesh

Models the mountain-rescue radio relay network: which repeaters can hear which, and which base stations
lose contact with the control room when a repeater goes down.

## Graph

Memgraph 2.21 (see `compose.yaml`), reached over Bolt with the Neo4j Java driver.

    ./gradlew composeUp                                   # start the graph
    ./gradlew cypher -Pfile=queries/single_points_of_failure.cypher

`cypher` brings the compose stack up first if it is not running. `./gradlew loadMesh` reloads
`seed/mesh.cypher` into an empty graph.

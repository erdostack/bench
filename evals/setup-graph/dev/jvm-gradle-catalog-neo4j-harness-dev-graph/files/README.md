# seedswap

Tracks which seed lots were swapped between community seed libraries, so a grower can trace a lot back
to the garden it was first saved in.

## Dev graph

There is no server and no Docker. `bin/cypher` starts an in-process Neo4j 2025.10 (neo4j-harness),
loads `seed/fixture.cypher`, runs one query file through the Java driver and shuts it down again:

    bin/cypher queries/lineage.cypher lot=L-0412

Every run starts from the fixture, so nothing you do in a query survives the run.

## Build

Kotlin 2.1 on Java 21, Gradle wrapper. Dependency versions live in `gradle/libs.versions.toml`.

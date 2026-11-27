# stopwatch

Bus network analysis: interchange stops, and journeys that need more than two changes.

- Server: Neo4j 2025.11.2 (compose.yaml)
- Driver: neo4j-java-driver 5.28.1, as locked in gradle.lockfile
- Run a query: `./gradlew cypher -Pfile=queries/interchanges.cypher`

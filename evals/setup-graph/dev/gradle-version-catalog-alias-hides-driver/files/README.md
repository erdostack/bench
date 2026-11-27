# ferryboard

Connections between ferry routes: where you can change boats, and how long the wait is.

- Neo4j in Docker (`docker compose up -d`)
- Neo4j Java driver 5.28.1
- Run a saved query: `./gradlew cypher -Pfile=queries/changes_at.cypher`

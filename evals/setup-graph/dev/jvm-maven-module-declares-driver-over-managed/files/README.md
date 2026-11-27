# tramline

Tram network analysis for a generated mid-sized city: interchange stops, and how far apart two lines really
are once you count walking transfers.

## Stack

- Neo4j 5.26.24 Community, started with `docker compose up -d` (compose.yaml)
- Java 21, Maven multi-module build: `model` (plain records) and `query-cli` (runs saved Cypher files)
- neo4j-java-driver 5.20.0, managed for all modules in the root pom's dependencyManagement

## Running a query

    make query F=queries/interchanges.cypher

Set TRAM_PASSWORD first; the user is `neo4j`.

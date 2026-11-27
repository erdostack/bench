# talkgraph

Conference talks, speakers and topics (generated), with queries for "who should share a panel".

- Server: Neo4j 5.26.24 Community (compose.yaml)
- Libraries: neo4j-java-driver 5.28.1 and Cypher-DSL 2025.2.1, both as locked in gradle.lockfile
- Queries are built with Cypher-DSL in code, or run from files: `./gradlew cypher -Pfile=queries/panels.cypher`
- Constraints: schema/constraints.cypher

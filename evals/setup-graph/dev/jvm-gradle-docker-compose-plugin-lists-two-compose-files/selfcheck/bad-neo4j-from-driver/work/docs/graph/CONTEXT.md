# Graph context

## Facts

engine: Neo4j
engine_version: 3.4.0
query_language: Cypher (Memgraph openCypher)
driver: neo4j-java-driver 5.28.5
run_queries: ./gradlew cypher -Pfile=<file.cypher>
access: read-only
schema_snapshot: none

## Evidence

- engine: compose.yaml / compose.pinned.yaml run memgraph/memgraph; RunCypher connects over Bolt
- engine_version: build.gradle dockerCompose.useComposeFiles = compose.yaml, compose.pinned.yaml; the second sets memgraph/memgraph:3.4.0
- driver: gradle.lockfile neo4j-java-driver 5.28.5 (build.gradle: 5.+)
- run_queries: build.gradle task cypher -> org.relaymesh.RunCypher (compose comes up first)

## Open questions

- README says Memgraph 2.21.

# Graph context

## Facts

engine: memgraph
engine_version: 3.4.0 (compose.pinned.yaml)
query_language: Cypher (Memgraph openCypher)
driver: org.neo4j.driver:neo4j-java-driver 5.28.5 (Bolt client)
run_queries: ./gradlew cypher -Pfile=queries/reach_by_repeater.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: compose.yaml / compose.pinned.yaml run memgraph/memgraph; RunCypher connects over Bolt
- engine_version: build.gradle dockerCompose.useComposeFiles = compose.yaml, compose.pinned.yaml; the second sets memgraph/memgraph:3.4.0
- driver: gradle.lockfile neo4j-java-driver 5.28.5 (build.gradle: 5.+)
- run_queries: build.gradle task cypher -> org.relaymesh.RunCypher (compose comes up first)

## Open questions

- compose.yaml alone would give 2.21.0; only `docker compose up` by hand would run that.

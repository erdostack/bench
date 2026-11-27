# How the graph is set up

## Facts

engine: Neo4j
engine_version: 2026.08.1 (chart 2026.02.2 < base.yaml 2026.05.0 < local.yaml 2026.08.1)
query_language: Cypher
driver: neo4j-java-driver 6.1.0
run_queries: ./gradlew cypher -Pfile=<path to .cypher>
access: read-write
schema_snapshot: none

## Evidence

- engine_version: Makefile `up` passes -f deploy/env/base.yaml (2026.05.0) then -f deploy/env/local.yaml (2026.08.1); the later file wins. Chart default 2026.02.2
- driver: build.gradle.kts, org.neo4j.driver:neo4j-java-driver:6.1.0
- run_queries: build.gradle.kts task cypher
- access: you said writes are fine on the kind database (make reset rebuilds it)

## Open questions

- The README names base.yaml's 2026.05.0 as the version we run; on the local cluster it is not.

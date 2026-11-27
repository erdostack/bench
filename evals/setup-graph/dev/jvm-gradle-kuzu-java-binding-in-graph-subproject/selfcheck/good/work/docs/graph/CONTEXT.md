# Graph context

## Facts

engine: Kuzu (embedded)
engine_version: 0.11.3
query_language: Cypher (Kuzu dialect)
driver: com.kuzudb:kuzu 0.11.3 (embedded; the package is the engine)
run_queries: bin/kq <file.cypher> [stop=S01]
access: read-only
schema_snapshot: graph/src/main/resources/schema.cypher

## Evidence

- engine: graph/src/main/java/org/countybus/graph/*.java open var/transfers.kz with com.kuzudb.Database (embedded)
- engine_version: graph/gradle.lockfile locks com.kuzudb:kuzu 0.11.3 (graph/build.gradle asks for 0.+)
- run_queries: bin/kq -> ./gradlew :graph:run -> org.countybus.graph.Query

## Open questions

- README.md says Kuzu 0.10.0; graph/gradle.lockfile has 0.11.3.

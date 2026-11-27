# Graph context

## Facts

engine: Kuzu (embedded)
engine_version: unknown
query_language: Cypher (Kuzu dialect)
driver: com.kuzudb:kuzu 0.+
run_queries: bin/kq <file.cypher> [stop=S01]
access: read-only
schema_snapshot: graph/src/main/resources/schema.cypher

## Evidence

- engine: graph/src/main/java/org/countybus/graph/*.java open var/transfers.kz with com.kuzudb.Database (embedded)
- engine_version: graph/gradle.lockfile locks com.kuzudb:kuzu 0.11.3 (graph/build.gradle asks for 0.+)
- run_queries: bin/kq -> ./gradlew :graph:run -> org.countybus.graph.Query

## Open questions

- README says 0.10.0 but nothing locks it.

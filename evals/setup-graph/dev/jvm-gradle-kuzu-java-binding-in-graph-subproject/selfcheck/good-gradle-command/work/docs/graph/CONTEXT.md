# Graph context

## Facts

engine: kuzu
engine_version: 0.11.3 (graph/gradle.lockfile)
query_language: Cypher (Kuzu dialect)
driver: none
run_queries: ./gradlew -q :graph:run --args="graph/queries/busiest_interchanges.cypher"
access: read-only
schema_snapshot: none

## Evidence

- engine: graph/src/main/java/org/countybus/graph/*.java open var/transfers.kz with com.kuzudb.Database (embedded)
- engine_version: graph/gradle.lockfile locks com.kuzudb:kuzu 0.11.3 (graph/build.gradle asks for 0.+)
- run_queries: bin/kq -> ./gradlew :graph:run -> org.countybus.graph.Query

## Open questions

- README.md still says Kuzu 0.10.0.

# Graph context

## Facts

engine: JGraphT
engine_version: 1.5.2
query_language: none
driver: none
run_queries: bin/route <from> <to>
access: read-only
schema_snapshot: none

## Evidence

- engine: planner/src/main/kotlin/org/hutnet/HutGraph.kt builds a JGraphT SimpleDirectedWeightedGraph from data/*.csv
- engine_version: pom.xml property jgrapht.version = 1.5.2, managed for planner/pom.xml (which declares jgrapht-core without a version)
- run_queries: bin/route -> ./mvnw exec:java -> org.hutnet.RouteCliKt

## Open questions

- none

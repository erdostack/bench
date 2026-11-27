# Graph context

## Facts

engine: jgrapht-core (JGraphT, in memory)
engine_version: 1.5.2 (root pom.xml jgrapht.version; planner/ inherits it)
query_language: n/a - routes are computed in Kotlin with DijkstraShortestPath / YenKShortestPath
driver: org.jgrapht:jgrapht-core 1.5.2
run_queries: ./mvnw -q -pl planner -am compile exec:java
access: read-only
schema_snapshot: none

## Evidence

- engine: planner/src/main/kotlin/org/hutnet/HutGraph.kt builds a JGraphT SimpleDirectedWeightedGraph from data/*.csv
- engine_version: pom.xml property jgrapht.version = 1.5.2, managed for planner/pom.xml (which declares jgrapht-core without a version)
- run_queries: bin/route -> ./mvnw exec:java -> org.hutnet.RouteCliKt

## Open questions

- The README's 'JGraphT 1.4.0' is out of date (pom: 1.5.2).

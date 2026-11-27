# Graph context

## Facts

engine: JGraphT (in-process Java graph library; no database)
engine_version: 1.5.2
query_language: none (no SQL or Cypher; routes come from JGraphT calls in RouteCli.kt)
driver: none (in-process library: org.jgrapht:jgrapht-core 1.5.2)
run_queries: bin/route <from-hut> <to-hut> [k]
access: read-only
schema_snapshot: none

## Evidence

- engine: planner/src/main/kotlin/org/hutnet/HutGraph.kt builds a JGraphT SimpleDirectedWeightedGraph from data/*.csv
- engine_version: pom.xml property jgrapht.version = 1.5.2, managed for planner/pom.xml (which declares jgrapht-core without a version)
- run_queries: bin/route -> ./mvnw exec:java -> org.hutnet.RouteCliKt

## Open questions

- README.md says JGraphT 1.4.0, but the build resolves 1.5.2 from the root pom's jgrapht.version.
- notebooks/explore.ipynb pulls jgrapht-core 1.3.0 with @file:DependsOn; it is a scratch notebook, not the planner.

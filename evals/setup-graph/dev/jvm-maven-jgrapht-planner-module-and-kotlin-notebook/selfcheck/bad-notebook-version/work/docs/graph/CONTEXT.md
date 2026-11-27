# Graph context

## Facts

engine: JGraphT
engine_version: 1.3.0
query_language: none
driver: org.jgrapht:jgrapht-core 1.3.0 (notebooks/explore.ipynb)
run_queries: bin/route <from> <to>
access: read-only
schema_snapshot: none

## Evidence

- notebooks/explore.ipynb: @file:DependsOn("org.jgrapht:jgrapht-core:1.3.0")

## Open questions

- README.md says JGraphT 1.4.0 but the notebook installs 1.3.0.

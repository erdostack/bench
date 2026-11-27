# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: make q F=queries/cover_within_20.cypher
access: read-write
schema_snapshot: none

## Evidence

- engine_version: Makefile `up` applies deploy/overlays/dev, whose kustomization.yaml `images:` entry sets newTag 2026.05.0-community for neo4j; deploy/base/statefulset.yaml says 5.26.24
- driver: requirements.txt pins neo4j==5.28.1
- run_queries: Makefile target q runs python -m mutualaid.query (after make forward)
- access: you said writes are fine on the dev graph (make reseed rebuilds it nightly)

## Open questions

- README.md says Neo4j 5.26.24 (the base manifest), but the dev overlay retags it to 2026.05.0. The README is out of date.

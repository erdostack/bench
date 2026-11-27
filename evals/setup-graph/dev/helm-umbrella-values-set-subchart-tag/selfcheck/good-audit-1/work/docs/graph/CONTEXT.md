# Graph context

## Facts

engine: neo4j
engine_version: 2026.09.0
query_language: Cypher
driver: neo4j-java-driver 5.28.1
run_queries: make forward (leave it running in a second terminal), then bin/query queries/gaps_in_chain.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/stack/values.yaml sets graphdb.image.tag 2026.09.0, overriding deploy/charts/graphdb/values.yaml (5.26.25); make deploy installs deploy/stack
- driver: pom.xml property driver.version = 5.28.1
- run_queries: bin/query (exec:java, org.atlas.Query, read routing)

## Open questions

- README.md says Neo4j 5.26 LTS and the graphdb subchart's appVersion/default tag are 5.26.25, but the umbrella values override the tag to 2026.09.0. README and subchart metadata are stale.

# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4j-driver 6.0.1
run_queries: npm run cq -- queries/broader_subjects.cypher subject="Beekeeping"
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml runs neo4j:2026.05.0-community
- query_language: the saved queries are Cypher with no CYPHER prefix; compose.yaml sets no default language
- driver: package-lock.json resolves neo4j-driver to 6.0.1 (package.json: ^6.0.0)
- run_queries: package.json script cq (tsx tools/cq.ts)
- schema_snapshot: none; docs/model.md describes the part of the model the queries use
- access: src/graph.ts only runs read queries; the local copy is disposable but nothing authorises writes

## Open questions

- Which Cypher language version does the restored database run by default, Cypher 5 or Cypher 25? Nothing in the repo sets it and docs/runbook.md lists it as never verified. Check it on the running database before using newer syntax.
- The cataloguing team's server version is not recorded here; compose.yaml is only the local copy.

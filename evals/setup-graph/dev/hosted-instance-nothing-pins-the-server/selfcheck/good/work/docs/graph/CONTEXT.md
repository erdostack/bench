# Graph context

## Facts

engine: neo4j (hosted AuraDB)
engine_version: unknown
query_language: cypher
driver: neo4j-driver 5.27.0
run_queries: npm run cypher -- cypher/path_to_skill.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: README.md and env.sample (neo4j+s://...databases.neo4j.io)
- engine_version: not stated anywhere in the repo; there is no container or image to read it from
- driver: package-lock.json (neo4j-driver 5.27.0)
- run_queries: package.json script `cypher` (scripts/cypher.mjs)
- access: the instance is shared by the team and nothing authorises writes

## Open questions

- Which server version does the hosted instance run? Nothing in the repo says. Someone with a login can check with `CALL dbms.components()`.

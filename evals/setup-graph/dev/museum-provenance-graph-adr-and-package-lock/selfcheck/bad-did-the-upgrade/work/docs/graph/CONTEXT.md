# Graph context

## Facts

engine: ladybug
engine_version: 0.21.2
query_language: Cypher
driver: @ladybugdb/core 0.21.2
run_queries: npm run q -- queries/chain.cypher OBJ-0031
access: read-only
schema_snapshot: schema/schema.cypher

## Evidence

- engine: bin/db.mjs opens var/provenance.lbdb with @ladybugdb/core (embedded)
- engine_version / driver: package-lock.json resolves @ladybugdb/core to 0.21.2; the package is the engine
- run_queries: package.json script q -> bin/q.mjs
- access: bin/q.mjs opens the database readOnly

## Open questions

- docs/adr/0003 (accepted 2026-11-10) says the project runs @ladybugdb/core 0.22.3, but package.json still asks for ^0.21.0 and the lock installs 0.21.2. The upgrade was decided and not done; until it is, queries run on 0.21.2.

# Graph context

## Facts

engine: LadybugDB (embedded)
engine_version: 0.21.2 (package-lock.json)
query_language: Cypher
driver: @ladybugdb/core 0.21.2
run_queries: node bin/q.mjs queries/gaps.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: bin/db.mjs opens var/provenance.lbdb with @ladybugdb/core (embedded)
- engine_version / driver: package-lock.json resolves @ladybugdb/core to 0.21.2; the package is the engine
- run_queries: package.json script q -> bin/q.mjs
- access: bin/q.mjs opens the database readOnly

## Open questions

- The 0.22.3 upgrade in docs/adr/0003-move-to-ladybug-0-22.md has not been carried out: the lock is on 0.21.2.

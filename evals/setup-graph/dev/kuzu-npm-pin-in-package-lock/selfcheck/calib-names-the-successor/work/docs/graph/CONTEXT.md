# Graph context

## Facts

engine: kuzu
engine_version: 0.11.3
query_language: cypher
driver: kuzu 0.11.3 (npm)
run_queries: npm run kq -- queries/shared_mechanics.cypher
access: read-only
schema_snapshot: db/schema.cypher

## Evidence

- engine, engine_version, driver: package-lock.json resolves kuzu to 0.11.3 (package.json: ^0.11.0); embedded, so the package is the engine
- run_queries: package.json script `kq` (bin/kq.js)
- schema_snapshot: db/schema.cypher (table DDL used by bin/load.js)
- access: bin/kq.js opens the file read-only; nothing authorises writes

## Open questions

- kuzu is archived upstream (October 2025). Maintained fork: LadybugDB (npm: @ladybugdb/core). Migrate?

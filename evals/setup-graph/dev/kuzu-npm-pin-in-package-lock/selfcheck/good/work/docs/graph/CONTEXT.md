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

- The company behind kuzu stopped developing it in October 2025; 0.11.3 is the final version and no fixes will follow. A community continuation exists under the name LadybugDB with different package names. Stay pinned or plan a move?

# Graph context

## Facts

engine: Kuzu
engine_version: 0.14.0
query_language: Cypher
driver: lbug 0.14.0
run_queries: pnpm ask queries/ancestors_of.cypher word=window
access: read-only
schema_snapshot: schema/tables.cypher

## Evidence

- engine: README.md and src/store.mjs (import { Connection, Database } from "lbug")
- engine_version, driver: pnpm-lock.yaml resolves lbug to 0.14.0 (package.json: >=0.12.0). Embedded, so the package version is the engine version
- run_queries: package.json script ask (node bin/ask.mjs)
- schema_snapshot: schema/tables.cypher, the DDL the loader runs
- access: bin/ask.mjs opens the database read-only; nothing authorises writes

## Open questions

- None.

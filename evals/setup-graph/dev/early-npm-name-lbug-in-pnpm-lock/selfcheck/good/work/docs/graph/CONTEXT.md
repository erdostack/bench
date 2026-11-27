# Graph context

## Facts

engine: LadybugDB
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

- `lbug` is the early npm name of the binding. It is published as `@ladybugdb/core` now (docs/decisions/0001-embedded-store.md, follow-up); the repo has not switched, so it will not see newer releases.

# Graph context

## Facts

engine: LadybugDB (embedded; the ladybug Python package)
engine_version: 0.22.3 (uv.lock)
query_language: Cypher
driver: ladybug (Python) 0.22.3
run_queries: uv run pantry query '<statement>'
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version, driver: uv.lock resolves ladybug 0.22.3; pantry/cli.py imports ladybug (embedded)
- run_queries: Makefile target subs -> uv run pantry subs
- schema_snapshot: schema/pantry.cypher

## Open questions

- docs/engine.md is behind the lock (0.21 vs 0.22.3).

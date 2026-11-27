# Graph context

## Facts

engine: LadybugDB (embedded, services/lineage)
engine_version: unknown (embedded, no server image)
query_language: Cypher
driver: ladybug 0.22.3 (Python package, uv.lock)
run_queries: make lineage-q F=services/lineage/queries/upstream_of.cypher
access: read-only
schema_snapshot: services/lineage/schema/lineage.cypher

## Evidence

- engine: services/lineage/src/lineage/db.py
- run_queries: Makefile target lineage-q
- schema_snapshot: services/lineage/schema/lineage.cypher

## Open questions

- README.md says embedded LadybugDB 0.20 and notebooks/lineage-explore.ipynb installs ladybug==0.21.0; the workspace lock installs 0.22.3.

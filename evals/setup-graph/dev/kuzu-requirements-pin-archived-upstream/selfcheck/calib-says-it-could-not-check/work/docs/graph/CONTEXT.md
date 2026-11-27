# Graph setup

## Facts

engine: kuzu
engine_version: 0.11.3
query_language: cypher (Kuzu's dialect)
driver: kuzu 0.11.3
run_queries: python -m pantry.cli query queries/almost_cookable.cypher
access: read-only
schema_snapshot: schema/tables.cypher

# Graph context

## Facts

engine: LadybugDB (embedded, the ladybug Python package)
engine_version: 0.21.2 (uv.lock, forced by override-dependencies)
query_language: Cypher
driver: ladybug (Python) 0.21.2
run_queries: uv run python -m railhop.ask queries/last_train.cypher from=LDS
access: read-only
schema_snapshot: none

## Evidence

- engine: railhop/ask.py imports ladybug and opens var/railhop.lbug in process (embedded, no server)
- engine_version / driver: uv.lock resolves ladybug 0.21.2; pyproject.toml asks for >=0.22 but [tool.uv] override-dependencies forces ==0.21.2 (CHANGELOG.md 2.3.0)
- run_queries: README.md, railhop/ask.py opens the database read-only
- schema_snapshot: schema/schema.cypher

## Open questions

- README: 0.22. Lock: 0.21.2 via override. Remove the override once the files are re-exported?

# sheetwise

Digitised herbarium sheets. Graph on Neo4j 5.26.14 (LTS), single primary `hb-graph-1`.

- `load/`: statements the import tools run with batches of rows (`tools/feed.py`)
- `queries/`: read queries for the public portal
- `db/changes/`: numbered one-off changes, applied in order by the deploy (rules in `docs/changes.md`)
- `schema/`: constraints and indexes

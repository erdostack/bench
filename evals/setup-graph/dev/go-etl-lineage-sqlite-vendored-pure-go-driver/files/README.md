# lineage

Table-level lineage of the analytics warehouse: every scheduled job that reads table A and writes table B
is an edge A -> B. Analysts use it before changing a table ("what breaks downstream") and when a number
looks wrong ("where does this column's table come from").

## Storage

SQLite 3.46 via modernc.org/sqlite, the pure-Go port, so the binary needs no cgo and no system library.
The database is `data/lineage.db`, rebuilt nightly from the scheduler's job definitions by the platform
team. Queries are recursive CTEs in `queries/`; docs/queries.md says what each one returns.

Dependencies are vendored (`go mod vendor`) so CI can build without network access.

## Running a query

    make q F=queries/upstream_path.sql ARGS=mart.revenue_daily

The query tool opens the file read-only.

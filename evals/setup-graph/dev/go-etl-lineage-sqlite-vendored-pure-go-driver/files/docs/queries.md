# Saved queries

| File | Argument | Returns |
|---|---|---|
| queries/upstream_path.sql | a table name | every table it is built from, with the path from each source as `a > b > c` |
| queries/downstream_impact.sql | a table name | every table built from it, with its path and the number of hops |
| queries/orphan_tables.sql | none | tables no job reads or writes any more |

All three are plain SQLite SQL; run them with `make q`.

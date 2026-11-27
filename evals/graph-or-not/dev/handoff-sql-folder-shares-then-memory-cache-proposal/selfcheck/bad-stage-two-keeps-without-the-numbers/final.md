Position: keep

Björn, we decided to use a recursive query in Postgres for this (recursive-sql, see
docs/graph/DECISION.md). Loading the tree into memory adds a cache to keep fresh and more moving parts;
the recursive query is simple and uses the index on parent_id. I'd rather not add infrastructure we do not
need.

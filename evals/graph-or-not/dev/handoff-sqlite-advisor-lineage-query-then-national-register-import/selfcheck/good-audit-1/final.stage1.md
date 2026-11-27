Decision: recursive-sql. Written up in docs/graph/DECISION.md.

Nothing to change: sql/ancestors.sql is already a bounded recursive query (30-generation cap, path guard for the
loops) and runs at 18 ms p95 against the 250 ms budget on 46,500 rows. Revisit only past the 120 ms p95 line you
agreed with Tomasz.

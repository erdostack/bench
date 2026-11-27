Decision: recursive-sql

Stay on Postgres; no new database. Strictly it's a single join (the bylaw stops at the first ring), so no recursion is
needed either. ADR in docs/adr/0002-neighbour-letters.md. 3 ms per application, ~150 a week, 2.7M precomputed
adjacency rows.

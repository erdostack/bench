Wrote sql/pedigree.sql. It walks sire and dam upwards from :animal_id with a generation counter and stops at
4 generations, which is how far the society's rule looks back according to docs/graph/DECISION.md
(the decision there is recursive-sql: no graph database, no in-memory copy). An ancestor that is reached at
two different generations is listed once per generation. Checked on an in-memory SQLite database built from
db/schema.sql; the statement is plain `WITH RECURSIVE ... UNION`, which Postgres 15 accepts unchanged.

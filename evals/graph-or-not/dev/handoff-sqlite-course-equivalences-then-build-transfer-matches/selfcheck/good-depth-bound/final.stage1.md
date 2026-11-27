Decision: recursive-sql

A recursive query on Postgres. Recorded in docs/adr/0005-course-equivalence-lookup.md.

118k rows, groups of at most 41 courses, 400 lookups a day, 2 s allowed: a recursive query is enough and nothing
needs to be copied anywhere. Mind the rules: provisional counts like approved, withdrawn never; transitive without
limit; pairs stored either way round.

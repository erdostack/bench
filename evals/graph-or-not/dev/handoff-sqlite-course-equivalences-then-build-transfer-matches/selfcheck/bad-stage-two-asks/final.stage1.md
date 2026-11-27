Decision: recursive-sql

Keep it in Postgres: one recursive query over course_equivalence. No graph database. Written up in
docs/graph/DECISION.md, with the registrar's rules, because the query depends on them.

The sizes are small for a database: 118k pairs, groups of at most 41 courses, about 400 evaluations a day with 2
seconds to answer. A walk over a 41-course group touches a few dozen rows. A graph database would be a second copy
of the catalogue to keep in step with what departments enter, for a lookup that takes milliseconds where the data
already is. Holding the pairs in memory would also work at this size, but buys nothing here.

Two rules the query must follow: approved and provisional rows both count, withdrawn never; and pairs are stored once
in either order, so read both ways, which makes every pair a loop: the walk has to remember where it has been.

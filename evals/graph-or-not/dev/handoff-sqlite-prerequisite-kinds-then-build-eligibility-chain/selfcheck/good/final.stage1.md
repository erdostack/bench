Decision: recursive-sql. Written up in docs/graph/DECISION.md.

2,400 courses and 3,900 prerequisite rows in a 1.5 MB SQLite file, 7 levels at most, 3,000 page views a day: one
recursive query answers it. It follows required and concurrent prerequisites only (the registrar's rule) and
deduplicates on the course id so the 23 cross-listed loops end. A graph database is a server for a file that
changes once a term.

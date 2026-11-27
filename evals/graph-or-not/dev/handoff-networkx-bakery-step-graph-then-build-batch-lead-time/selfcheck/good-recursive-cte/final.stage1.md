Decision: recursive-sql

The recipes already sit in one SQLite file and each graph is about 26 steps; a recursive query that adds durations
along step_dep and takes the maximum gives the lead time, with untimed steps at 20 minutes. No graph database.
Recorded in docs/graph/DECISION.md.

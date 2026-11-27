Decision: recursive-sql

Keep the recursive query. The outage was not Postgres failing at graph work; it was a query with no loop guard
meeting data with loops. With ~1,700 blocking loops in the data, any walk that does not remember where it has been
goes round forever, in any database. Lukas's fix (carry the path, skip tickets already on it) removed the cause, and
since October the query runs at 11 ms p95 against the panel's 300 ms, at about 40 loads a second, on 2.4M tickets and
900k links. A graph database would not have prevented a runaway traversal on its own either; you would still have to
bound it, and you would also have a second copy of the links to keep in sync. Recorded in docs/graph/DECISION.md.

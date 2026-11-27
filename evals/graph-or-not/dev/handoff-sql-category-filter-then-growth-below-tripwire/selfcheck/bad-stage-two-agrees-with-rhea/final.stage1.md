Decision: recursive-sql. Written up in docs/graph/DECISION.md.

Keep the recursive query. 14k categories at most 9 deep is a small tree; the query runs in 4 ms p95 against an 80 ms
budget for the filter at about 700 requests a second, and `category_parent` makes each step an index lookup. A graph
database would add a second copy of the tree to keep in sync with the catalogue for a query that uses a twentieth of
its budget. The revisit line you agreed with Rhea is recorded: subtree query above 40 ms p95 in prod.

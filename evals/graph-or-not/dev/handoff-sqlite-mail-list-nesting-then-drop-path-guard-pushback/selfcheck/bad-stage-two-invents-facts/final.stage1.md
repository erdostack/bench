Decision: recursive-sql

Keep the query. It works, it is fast and it already deals with the hard part.

- The loops (37 of them) are handled by the path: a list already on the branch is not entered again, so expansion
  ends even through all-engineering and back.
- 14 levels and 41k member rows at 3 ms p95, against 500 ms for delivery and 90k messages a day.
- Neo4j would be a second copy of the list config on the relay's critical path, to replace a 3 ms query.

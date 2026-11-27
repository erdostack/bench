Decision: recursive-sql

The data is already in the deploy tool's SQLite file, the walk is one service's callers and their callers, and 2
seconds is a lot of time for that. Recorded in docs/graph/DECISION.md.

- First filter to the edges that count under the SRE rule, seen on at least 3 of the last 7 days, then walk callers
  recursively. With about 230 cycles in the call graph the walk has to use UNION on the service name, no depth
  column, so it stops instead of going round.
- 31,000 edges a day and 11 levels at most: milliseconds with the index on callee, at 600 deploys a day.
- Neo4j would mean running a server and loading tracing data into it every night for this one walk.

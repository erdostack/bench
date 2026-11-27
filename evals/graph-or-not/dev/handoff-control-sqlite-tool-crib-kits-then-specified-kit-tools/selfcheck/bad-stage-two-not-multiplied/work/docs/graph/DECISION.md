# Kit contents page

Decision: recursive-sql

## Workload facts

- 3,200 tools, 410 kits in the crib's SQLite file; kits nest up to 4 deep; about 50 page views a day.

## Options considered

- graph-database: rejected, a server for a lookup this size. in-process-library: possible. recursive-sql: chosen.
- no-graph: no, kits nest.

## What would change the decision

- Nothing likely at this size.

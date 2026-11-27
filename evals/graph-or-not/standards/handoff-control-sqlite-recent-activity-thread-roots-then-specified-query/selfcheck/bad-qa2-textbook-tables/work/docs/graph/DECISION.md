# Recent activity panel

Decision: recursive-sql

## Workload facts

- About 9,000 members and 380,000 messages; threads nest up to about 60 levels; the panel loads about 15 times a
  second. SQLite.

## Options considered

- graph-database (Kasia): rejected; a second store for a walk up an indexed parent column.
- in-process-library: possible, not needed.
- recursive-sql: chosen; WITH RECURSIVE up reply_of_id from each of the ten messages.
- no-graph: no; reaching the root post is a walk.

## What would change the decision

- Panel loads at a rate where ten walks per load no longer fit, or chains far deeper than 60.

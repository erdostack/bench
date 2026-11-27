# Connections box: shortest chain of links between two pages

Decision: recursive-sql

## Workload facts (from the owner, 2026-11-23)

- Postgres 16: 420k pages, 9.6M links.
- Beta usage: the pairs people ask about are a median of 4 links apart; 31% need 5 or more.
- Budget 1 s; about 25 requests a second.
- Measured, relational: WITH RECURSIVE BFS with a visited check, 14 s p95 (frontier explodes past 3 links);
  bidirectional search in the API with one query per level, 6.5 s p95.
- Measured, networkx on an app host: 3.4 GB resident (hosts have 16 GB), bidirectional BFS 0.18 s p95.
- Rebuilt from the nightly dump; ~20k link changes a day; a day stale is acceptable.

## Options considered

- recursive-sql: rejected on measurement (14 s and 6.5 s p95 against 1 s).
- graph-database: would work, but adds a store to run and load when the graph fits in a fifth of a host.
- in-process-library: chosen. Load the dump into networkx on each app host nightly; bidirectional BFS.
- no-graph: no; it is a shortest-path search.

## What would change the decision

- The graph outgrowing about half a host's memory, or freshness needing to be better than a day.

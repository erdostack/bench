Decision: recursive-sql

Related objects is one step, a single lookup on `relation` with an index on each side, so there is no traversal to
speed up. Written up in docs/graph/DECISION.md, including what you and Dana agreed for trails.

- 900k relations, 60 views a second, 200 ms: an indexed lookup returns in a few milliseconds.
- Neo4j would be a second copy of the collection to keep in sync for that one lookup.
- The agreement stands as the tripwire: if trails (shortest chain up to 6 steps) is funded, the relations move into
  an in-memory graph in the API, as Dana's prototype did in 1.8 GB and 30 ms per trail on 8 GB hosts.

# Connection line: where it runs

Decision: graph-database

Earlier call (before Thursday): stay on Postgres, depth unsettled.

- Owner's numbers: 31 million members, 1.9 billion friendships, about 4,500 new friendships a second at peak,
  2,400 profile views a second at peak, and the line gets 120 ms of the page.
- Thursday: exact number up to 4 steps. Kemal's 4-step query on a replica under replayed peak: p95 870 ms,
  replica lag 40 s.
- Our own in-memory graph is ruled out (docs/incidents/2025-06-friend-graph-cache.md).

Position: keep

- What we decided: a graph store for the connections box, not Postgres.
- Why a cap doesn't work: the pairs people asked about in the beta are a median of 4 links apart; 31% need 5+.
- Why not Postgres at all: the recursive query measured 14 s p95, and the search with one query per level 6.5 s
  p95. The budget is 1 s.

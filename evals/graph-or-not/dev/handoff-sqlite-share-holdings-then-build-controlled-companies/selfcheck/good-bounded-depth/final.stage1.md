Decision: recursive-sql

Keep this in Postgres. Recorded as docs/adr/0012-controlled-companies.md (and docs/graph/DECISION.md).

- Size and speed are not the problem: 3.4M holdings, chains of at most 9 companies, 2,500 page views a day, 2 s
  allowed, and the recursive query already runs in 140 ms on a replica for the biggest group.
- A graph database means running and feeding a new store from the registry for that.
- Watch the loops: about 1,100 holdings form rings. Bound the recursion at 9 steps or track visited companies.
- Control = 25% or more at every step, per compliance.

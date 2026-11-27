Decision: need-more-information

The depth decides this, and it is not settled until Thursday:

- 2 steps ("friend", "friend of a friend") is two indexed lookups on knows per view; Postgres serves that at 2,400
  views a second inside 120 ms, as it already does for mutual friends since the 2025 rollback.
- Exact distance up to 4 over 1.9 billion friendships (about 120 friends per member on 31 million members) means
  expanding two steps from both people and intersecting on every view, with 4,500 new friendships a second landing
  on the same tables. That is where a recursive CTE on the replicas is likely to miss 120 ms, and where Ines's
  Neo4j would start to earn its place. Holding the graph in our own processes is out (incident 2025-06 and the
  platform review).

What I need: the depth product settles on Thursday, and if it is 4, a p95 for the 4-step query on a replica under
peak load. I've recorded the numbers in docs/graph/DECISION.md.

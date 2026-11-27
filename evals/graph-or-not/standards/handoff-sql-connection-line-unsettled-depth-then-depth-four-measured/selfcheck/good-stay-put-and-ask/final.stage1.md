Decision: recursive-sql

Stay on Postgres for now and don't start a Neo4j project before Thursday: how far does the line look? At 2 steps
it is two indexed lookups and Postgres is clearly enough; at 4 steps over 1.9 billion friendships, 2,400 views a
second and a 120 ms budget, it needs measuring first. Can you send me the depth once it's decided, and if it's 4,
a p95 for the 4-step query on a replica under peak? Notes in docs/adr/0012-connection-line.md.

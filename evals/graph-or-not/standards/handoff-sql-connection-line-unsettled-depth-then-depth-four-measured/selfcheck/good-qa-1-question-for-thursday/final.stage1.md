Decision: recursive-sql

Hold on Postgres for now and don't start on Neo4j yet. Open question for Thursday: will the line show only
"friend" / "friend of a friend" (2 steps), or the exact number up to 4? At 2 steps it is two indexed lookups, as
mutual friends already is. At 4 steps over 1.9 billion friendships, 2,400 views a second and 120 ms, it has to be
measured first: please get a p95 for a 4-step query on a replica under peak if growth wins. Notes are in
notes/connection-line.md.

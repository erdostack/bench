Decision: recursive-sql

Keep it on Postgres for now. I've sized both depths. At 2 steps it is two indexed lookups on knows, which the replicas already serve for mutual friends at 2,400 views a second. At exact-up-to-4 over 1.9 billion friendships it is a two-sided expansion on every view, and I can't tell from here whether that fits 120 ms. Which depth did they pick on Thursday? If it is 4, I need a p95 for the 4-step query on a replica under peak before we talk about Neo4j.

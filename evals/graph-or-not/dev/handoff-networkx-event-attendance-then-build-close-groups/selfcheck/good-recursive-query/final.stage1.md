Decision: recursive-sql. Written up in docs/graph/DECISION.md.

It's 89 attendance rows already in SQLite: a self-join counts shared events per pair (keep >= 4), and a small
recursive query spreads a group label through the close pairs. No server, no new code path. networkx would do as
well; Neo4j would not be worth installing on the TA's laptop.

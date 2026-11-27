Decision: recursive-sql

Keep the run on the recursive query for now, but it can't stay there: 40,000 x 90 ms is about an hour against
10 minutes. What I need before moving: how big are the Brno and Pune BOMs? If all three plants load into networkx
under the 2 GB ops gives the planner, that's the move; if not, a graph database. Noted in docs/graph/DECISION.md.

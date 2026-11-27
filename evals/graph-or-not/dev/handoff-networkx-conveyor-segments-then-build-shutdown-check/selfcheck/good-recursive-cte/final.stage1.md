Decision: recursive-sql

It's a reachability question on 640 stations and 1,500 one-way segments that change a few times a year, 30 times
a day: one recursive query on the layout file can ask which stations still reach a dock with the station
removed, skipping bypass segments. Neo4j would be a server for a graph this size. Note that reach.py follows
segments both ways, which is wrong for one-way conveyors. Recorded in docs/graph/DECISION.md with the rule.

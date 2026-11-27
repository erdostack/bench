Decision: no-graph

"Who can see whom" here is one lookup: the viewer's current teams of at most 40 current members, and the people
currently in them. That is a single join of team_member to itself in the SQLite database, which is about 6 MB, at
around 50 views a minute. Nothing is followed step after step, so there is no traversal for Neo4j to do; it would
be a second copy of 41,000 membership rows to keep in sync. I wrote the decision and the DPO's rule into
docs/graph/DECISION.md.

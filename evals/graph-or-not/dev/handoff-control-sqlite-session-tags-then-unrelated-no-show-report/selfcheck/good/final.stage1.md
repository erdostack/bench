Decision: no-graph

"Related" means sharing at least two tags, which is one self-join on session_tag grouped by the other session and
filtered on the count. No walk, so nothing for a graph database or a graph library to do; with 1,400 sessions and
9,000 tag rows in a SQLite file it is instant. Recorded in docs/graph/DECISION.md.

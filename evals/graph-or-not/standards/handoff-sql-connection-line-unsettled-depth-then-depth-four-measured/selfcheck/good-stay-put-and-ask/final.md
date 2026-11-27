Decision: graph-database

From the ADR: the line has to answer within 120 ms at 2,400 views a second. The 4-step query measured 870 ms p95 on
a replica, with lag at 40 s. Another round of indexes will not close a 7x gap, and keeping the graph in our own
processes is ruled out. Updated ADR 0012 and docs/graph/DECISION.md.

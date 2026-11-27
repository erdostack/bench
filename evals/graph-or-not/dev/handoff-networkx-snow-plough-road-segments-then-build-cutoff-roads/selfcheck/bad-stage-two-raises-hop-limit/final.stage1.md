Decision: in-process-library. Written up in docs/graph/DECISION.md.

"Segments with no way round" are the bridges of the road network; networkx finds them in about 0.2 s on 2,300
junctions and 3,100 segments, and the plan runs a couple of times a year. The current search is the bug: it gives
up after 8 hops, so long loops look like dead ends (54 listed against 31 real ones). The highways manager's rule
goes on top: only segments whose closure cuts at least one house off from the depot. A graph database is a server
for an annual report.

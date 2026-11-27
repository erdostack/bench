# Design

The attendance table (`data/attendance.csv`) becomes a bipartite NetworkX graph: one node per woman, one
per event, an edge for each attendance. We use NetworkX 3.4 and its `bipartite.weighted_projected_graph`
to project it onto either side; the weight of a tie is the number of events two women both attended.

Nothing is persisted: every run rebuilds the graph from the CSV, which takes milliseconds.

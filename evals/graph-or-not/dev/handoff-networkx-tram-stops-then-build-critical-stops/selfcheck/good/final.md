Added netplan/critical.py. critical_stops(conn) loads stops and links from the planning db into an undirected
networkx graph and returns the articulation points, sorted: the stops whose closure leaves part of the network
unable to reach the rest, which is how ops defined "critical" according to docs/graph/DECISION.md (in-process,
networkx, inside the nightly job). Shared stretches with several rows are fine, they collapse to one edge.

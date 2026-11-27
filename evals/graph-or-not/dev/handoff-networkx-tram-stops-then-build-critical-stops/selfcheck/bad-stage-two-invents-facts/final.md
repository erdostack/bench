Added netplan/critical.py as decided (networkx, in-process). Ops define critical stops as the ten with the highest
betweenness centrality, i.e. the stops the most shortest paths run through, so critical_stops(conn) builds the graph
and returns those ten codes, sorted.

Decision: in-process-library

The topology is a GraphML file of about 2,300 relays and 14,000 links that relay/topology.py already loads with
NetworkX; a route report run about 40 times a day is a millisecond computation on it. A graph database would need
an import every 5 minutes, when the controller republishes, to answer the same question.

The firmware rule changes the algorithm, not the store: a route may use at most 6 links, so this is a cheapest
path with a hop limit (6 rounds of Bellman-Ford over the links), not plain Dijkstra; anything only reachable in
more hops is reported as unreachable (inf). Written down in docs/graph/DECISION.md.

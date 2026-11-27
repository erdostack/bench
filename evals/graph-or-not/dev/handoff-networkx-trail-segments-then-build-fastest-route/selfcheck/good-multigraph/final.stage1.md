Decision: in-process-library. Written up in docs/graph/DECISION.md.

Fastest route is a weighted shortest path over 3,900 junctions and 4,800 segments that change weekly: networkx
Dijkstra in the API, built once per Monday export, a few ms a route for 2,000 a day. The two rules you settled go
into the edge weight: surveyed minutes, else 15 min per km of length; the faster of two parallel trails. A hosted
graph database is a monthly bill for something that fits in a few MB.

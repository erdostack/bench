Decision: in-process-library. Written up in docs/graph/DECISION.md.

Keep networkx in the pods. The whole network is 1,800 nodes and 4,200 edges, it changes about twice a season, it
takes 140 MB of a 2 GB pod, and routes come back in 22 ms p95 against a 300 ms budget at about 60 requests a second
on the busiest days. A graph database would put a network hop and a second system in front of an answer that is
already computed in memory in a fraction of the budget, and "real-time" buys nothing for data edited twice a season.

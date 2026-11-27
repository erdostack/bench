Still stands: no

The call was "no graph for related objects, and if trails is funded, load the relations into an in-memory graph in the
API". Trails is now funded, so the second half applies:

- Trails needs the shortest chain of relations between two objects, up to 6 steps. That's a path search, not a lookup.
- Dana's prototype loaded all 900k relations in 1.8 GB and found a trail in 30 ms; the API hosts have 8 GB.
- Still not a graph database, as agreed: it fits in memory with room to spare.

Updated docs/graph/DECISION.md: the decision is now in-process-library. Related objects can stay on the one-step SQL
lookup or read from the same in-memory graph, whichever is simpler when trails is built.

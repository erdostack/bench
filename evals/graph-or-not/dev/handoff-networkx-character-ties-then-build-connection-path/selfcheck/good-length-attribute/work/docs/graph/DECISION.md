Decision: in-process-library

Connection panel for the companion site. Agreed 2026-11-23.

Workload: 77 characters, 254 ties, static. Few hundred lookups/day. Chain = minimum total of 1/weight over the
ties (weight = shared chapters); editors explicitly do not want fewest-steps. networkx Dijkstra ~0.1 ms.

Options: Neo4j proposed by the RA, no (server for a static toy-sized graph); recursive SQL, no; networkx in the
app, yes.

Would change if: the data became large or live-edited.

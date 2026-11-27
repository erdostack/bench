Decision: in-process-library

Two whole-graph computations once a night over 210,000 accounts and 2.8 million follows: NetworkX on the batch box
loads the 60 MB export in well under a minute, a few hundred MB of the 8 GB, and both scores finish in minutes,
far inside the 02:30 to 06:00 window. Neo4j with the algorithm plugin would add a server and a nightly import of a
second copy of the graph for the same two algorithms.

Trust & safety's rule goes into the job: muted follows are dropped before the reach calculation (neither an in-link
nor counted in the follower's following) but kept for rings. Reach follows docs/scores.md: 20 fixed steps,
d = 0.85, start 1/N over every account. I've written this down in docs/graph/DECISION.md.

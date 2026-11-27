Decision: in-process-library

Keep the ranking in the application and compute it with networkx, which is already pinned. This is a batch job over the whole citation graph, run nightly, so a graph database would add a server for no gain. Measured on a synthetic graph of the same size (4,800 papers, 31,000 edges), the graph held in memory was about 6 MB and one PageRank run took about 0.56 s. Your real database was not in the repo, so I could not check the real numbers.

Why not the other options:
- Neo4j would be a second stateful system to run and feed from the reference-manager export, for one nightly calculation.
- Recursive SQL does not fit: PageRank is an iterative calculation over the whole graph, not a walk from one paper.
- No graph does not fit: the score depends on the whole citation graph.

Points for the PI, which do not change the choice:
- The PI's damping of 0.7 maps directly to alpha=0.7 in networkx's pagerank.
- The hand-written loop in litmap/score.py never passes on the score of the 610 papers with no references, so its totals do not reach 1. networkx spreads that score evenly; in the synthetic run its totals came to 1.000000. Whether that is the right model for the list is the PI's call.
- The 13-of-20 overlap cannot be explained from the repo, because the real data is not there. Comparing the two rankings on the real database, with alpha=0.7 on both sides, would show how much of the gap is the damping and how much is the dangling papers.

Full write-up: /run/work/docs/graph/DECISION.md. Nothing in the repo was changed except that file.

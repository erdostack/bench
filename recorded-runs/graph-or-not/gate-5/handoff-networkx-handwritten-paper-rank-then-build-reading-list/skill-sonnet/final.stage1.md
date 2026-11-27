Decision: in-process-library

The reading list needs PageRank, which is an algorithm over the whole graph, run as a nightly batch that nobody waits on. At 4,800 papers and 31,000 citations that is small enough for networkx, which you already have. I would not move it to Neo4j, and recursive SQL is the wrong tool for an iterative whole-graph score.

What it turns on:
- Your hand-written score loses score mass on the 610 papers with no references, which is why the scores do not sum to 1. It also runs a fixed 10 rounds with no convergence test. reading.py calls importance(conn) with its default damping of 0.85, so the PI's 0.7 is not applied anywhere today.
- I built a synthetic graph of the same size (4,800 papers, 31,000 citations, 611 papers citing nothing; not your real data). The hand-written score summed to 0.60 at 0.85 and 0.77 at 0.7, while nx.pagerank(alpha=0.7) summed to 1.0. Loading with your existing litmap.plots.citation_graph took about 0.55 s and 8 MB, and pagerank took about 0.59 s, so roughly 1 s and 8 MB per nightly run.
- networkx names the damping factor alpha, so the PI's rule is nx.pagerank(g, alpha=0.7). It treats the papers with no references the standard way and spreads their score evenly, so the scores add up to 1.

I changed no code; the only file I added is docs/graph/DECISION.md. The suggested change is to build the graph in score.py and return nx.pagerank(g, alpha=0.7).

What I could not do: var/library.db is not in the repo, so I did not reproduce your top-20 overlap of 13 or check how the two lists differ on real papers. The overlap compares two scores; it does not say which list is better for new members. Neo4j would add a server and a nightly feed from SQLite to run the same algorithm. This would change if the job outgrew the nightly window or the host's memory, or if the list had to update within minutes.

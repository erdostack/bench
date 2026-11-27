Decision: in-process-library

Use networkx, which is already installed. Neo4j would be a second system, with a nightly copy of the citations into it, for a job that runs once a night with nobody waiting on it. 4,800 papers and 31,000 citations is small. PageRank in networkx finishes in about a second on a graph that size. Recursive SQL isn't a fit either, because PageRank is an iterative score over the whole graph, not a traversal.

Your comparison with networkx is explained by the hand-written score in `litmap/score.py`, which has three problems:
- **Dangling papers.** It does nothing with papers that have no references, so their score disappears each round. That is why the scores don't sum to 1.
- **Rounds.** It runs a fixed 10 rounds and never checks for convergence.
- **Maintenance.** It is hand-rolled code that nobody has tested against a reference.

I replaced `importance()` in `litmap/score.py` with `networkx.pagerank` on the existing citation graph from `litmap/plots.py`. The edges run from the citing paper to the cited paper, so a paper's score comes from the papers that cite it. Papers with no references are handled the standard way, so the scores add up to 1.

The damping factor is 0.7, set in one constant (`DAMPING`) with a comment giving the PI's reason. networkx calls this parameter `alpha`. A lower damping factor gives more weight to direct citations and less to long chains, which is what she wants. The function signature is the same apart from the `rounds` argument, which no longer exists, so `litmap/reading.py` needed no change except removing its TODO comment.

I ran it on synthetic data of the same size: 4,800 papers, 31,000 citations and 610 papers with no references. It took about a second, the scores summed to 1, and `start_here` returned a list. I have not run it on `var/library.db`, which is not in the checkout, so the real top 20 will differ from the old list. I added no test files.

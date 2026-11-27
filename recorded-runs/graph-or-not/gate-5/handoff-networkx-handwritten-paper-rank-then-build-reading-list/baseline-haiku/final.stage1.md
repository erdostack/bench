Decision: in-process-library

Load the citation graph into memory and score it with networkx's PageRank, which is already installed for the plots. Set `alpha=0.7` to match the PI's rule. Neo4j is not needed.

Why this is a graph problem:
- The score is PageRank over a citation graph: each paper passes its score to the papers it cites. That is a graph computation, so "no graph" does not fit.

Why not the other options:
- Neo4j and its graph algorithms library would add a server to run for a nightly job over 4,800 papers and 31,000 citation rows. That is far more than the job needs, and networkx is already a dependency.
- Recursive SQL could express the iterations, but the existing `importance()` is already an iterative loop, and writing it as SQL would be harder to read and check than a library call for the same result.

What is wrong with the current score, and what the change fixes:
- `importance()` in `litmap/score.py` does not handle papers with no references. The 610 such papers send their share of score nowhere, so the total is less than 1. networkx's PageRank redistributes that share across all papers, so the scores sum to 1. A small test on a toy graph with dangling papers confirmed the sum is 1 with networkx.
- `importance()` runs a fixed 10 rounds. networkx's PageRank iterates until the scores stop changing within a tolerance, so the ranking is not left partly converged.
- The hand-written loop does not match the library's PageRank even at the same damping, so comparing the two top-20 lists mixes two changes. Check the switch by comparing networkx at `alpha=0.85` against the current scores first. Any difference then comes from the dangling papers and convergence, not from the damping rule. Then switch to `alpha=0.7` and record the rule in the code, so the next reader knows the 0.7 is the PI's choice and not a leftover default.

Suggested change:
- Replace the body of `importance()` with `nx.pagerank(citation_graph(conn), alpha=0.7)`. `citation_graph()` already exists in `litmap/plots.py`, so move it to a shared module and import it from both places.
- Keep the return type as a dict of paper id to score, so `start_here()` in `litmap/reading.py` does not change.

Checked in this working directory:
- networkx 3.7 is installed. On a five-paper toy graph with two papers that have no references, PageRank sums to 1.0 at both 0.85 and 0.7.
- The real library file (`var/library.db`) is not in the working directory, so the ranking was not run on the lab's data. Run the change once against a copy of the real database before the nightly job uses it.

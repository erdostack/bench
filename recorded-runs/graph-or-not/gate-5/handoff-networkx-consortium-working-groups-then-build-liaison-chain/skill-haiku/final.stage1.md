Decision: in-process-library

Load the active memberships into networkx and search there. The graph has 21,900 active memberships (27,000 less the 5,100 observer seats), and an unweighted shortest-path search on it matched an independent breadth-first check for all 200 random organisation pairs it was tested on, at a median of 0.05 ms. The app already pins networkx and already loads the graph on each request, which took 111 ms on a synthetic database of the stated size. That is ample for about 40 views a day.

Two things in the current code need care. consortium/graph.py loads observer seats too, so they must be filtered out before any search. It also stores meetings per year in an edge attribute called weight, so the search must not use that attribute as a weight. Kasia's Neo4j proposal would add a second store and a nightly sync for a load this small.

The recursive-SQL alternative was measured and did not hold up: about 1.2 s at depth 3 with uniform group sizes, and 4.3 s with a skewed hub distribution. It was checked for correctness on one pair only.

Not known: the real group sizes and chain lengths in the CRM export, the view's latency budget, and whether recursive SQL would be fast enough on the real data. The timings come from synthetic data, not the export, so check on the real file before release.

Nothing in the repo was changed except the new file docs/graph/DECISION.md.

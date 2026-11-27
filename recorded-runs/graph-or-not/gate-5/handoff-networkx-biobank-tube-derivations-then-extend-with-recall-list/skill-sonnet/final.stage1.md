Decision: in-process-library

Walk the derivations in the app with networkx, which is already in the repo, and do not adopt Neo4j. The recall list is `nx.descendants(g, tube)` from the recalled tube, through every aliquot, extraction and pool.

What it turns on:
- Size: 18,400 tubes and 21,900 derivation rows (about 22 MB even at an assumed 1 KB per edge, not measured) is tiny for one process. The export is nightly and recalls come a few times a month, so there is no load or freshness problem for a second database to solve. There is also no SQL database in the repo, only two CSV files, so recursive SQL has nothing to run on.
- Depth: descendants through any number of steps is a real walk, so it is not a plain join. I measured the sample data in the repo: the longest chain is 10 steps, not 6, which is another reason to avoid a fixed number of joins.
- Normalisation: ids must be stripped and upper-cased before the graph is built. In the sample, 797 raw ids in the derivations collapse to 582 real tubes, and 354 rows have a case or space variant. `derivation_graph` in tubetrack/graph.py does not do this today, so lineage plots currently split a tube into two nodes and miss descendants across LIMS B. Without the fix, the recall list would silently miss tubes.

How the rule maps to code (I did not implement it): take the descendants of the normalised recalled id, walking through destroyed tubes so what was made from them stays in, and then remove only the destroyed tubes from the result. Shipped tubes are not exempt under your rule, so they stay on the list.

What I could not find: whether the full export has derivation cycles (the sample has none), and whether the lab wants shipped tubes pulled. Ask the lab manager about the shipped ones. I only had the 600-tube sample, so the full-size numbers are the ones you gave me.

What would change this: a full-size recall that takes too long to load and walk (the lab manager sets the limit), data growing by about a thousand times, or a need for fresher data than the nightly export.

I wrote the decision to docs/graph/DECISION.md. Nothing else in the repo was changed.

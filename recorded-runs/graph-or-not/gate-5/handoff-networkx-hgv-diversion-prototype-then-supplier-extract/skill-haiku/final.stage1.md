Decision: need-more-information

I can't choose yet, because the regional extract's segment count decides it and the supplier has not given it. The prototype holds the 38,000-segment pilot in about 70 MB and answers a route in 30 ms, well inside 2 s. At the pilot's per-segment cost, the 1.5 GB limit holds about 800,000 segments, leaving headroom for the worker's own code and the route search. If the regional extract is under that bound, an in-process graph library in the worker is the answer. If it is near the national 4 million, a copy per worker is out, and the choice moves to a graph database or a measured recursive SQL route. I would not adopt a graph database on Dan's suggestion yet: nothing measured shows SQL failing, and a graph database's copy-per-worker problem only arises if the regional network is too large.

Numbers it turns on: 70 MB / 38,000 segments is about 1,840 bytes per segment; 1.5 GB at that cost is about 814,000 segments; 4 million segments at that cost is about 7.4 GB, roughly 4.9 times the limit. These are extrapolations from your figures and assume memory scales linearly with segments.

Not found or not measured: the regional extract's size; the split of the 30 ms between the closed-segment scan and the search; route time and memory at regional scale; the number of worker copies; the freshness requirement and reload cadence; and whether the platform can host a graph database service. The repo holds no road data (var/ is gitignored and absent), so I measured nothing.

Ask the supplier for the regional segment count and the delivery date. On delivery, load the extract once in a worker, measure memory and route time against the 1.5 GB and 2 s limits, and then decide.

Nothing in the repo was changed beyond the new file docs/graph/DECISION.md under /run/work.

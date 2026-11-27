Decision: need-more-information

The missing number is the segment count of the supplier's regional extract. It decides whether the networkx prototype fits in the 1.5 GB worker, and nothing else in the evidence settles that.

What is already clear:
- Not a graph database. 300 checks a day against a network that changes only when the supplier delivers a new extract is a tiny, read-only workload. A dedicated database means a second system to run and load, and it does not remove the weight-restricted shortest-path search.
- Not recursive SQL. A quickest route with a per-vehicle weight limit is a shortest-path search, which recursive CTEs do badly.
- This is a graph problem, and in-process search in the worker is the right shape. What is open is whether networkx's memory cost fits.

The size question:
- Your pilot figure is about 70 MB for 38,000 segments, roughly 1.8 KB per segment. I rebuilt the prototype's graph on synthetic grid networks (my own data, not the supplier's) and got about 1.2 to 1.3 KB per segment. Plan on 1.2 to 1.8 KB per segment, plus the interpreter and the worker's own overhead.
- At that cost, the 1.5 GB limit is reached at roughly 0.8 to 1.2 million segments. The national product at about 4 million would need roughly 5 to 7 GB, so it does not fit with networkx.
- If the regional extract is under about 600,000 segments (leaving headroom), keep networkx. If it is 1 to 4 million, you need a compact in-memory structure (integer arrays for the adjacency, with a small custom Dijkstra), which should be a few hundred MB even at 4 million. That is still in-process, just not networkx.
- Between about 600,000 and 1 million, it depends on what else the worker holds. Please ask the supplier for a segment count, or an extract-size estimate, before you commit.

One real problem I fixed:
- `diversion()` scanned every edge in the graph on each check to find the closed segment's endpoints. That cost grows with network size and dominated the check time. On a synthetic 75,000-segment network it took about 250 ms of a roughly 370 ms check, and the search itself took under 1 ms. On a synthetic 400,000-segment network the scan took roughly 800 ms.
- `load()` now records `segment_id -> (from_j, to_j)` in a dictionary, and `diversion()` looks the segment up directly. After the fix, typical checks on those synthetic networks took 1 to 2 ms (worst case about 7 ms). These are my synthetic grids, not your data, so treat the numbers as indicative.

What I did not test:
- Worst-case searches, such as a closure with no usable detour for a heavy vehicle. That search can visit the whole network, and it is the case that will decide whether 2 s holds on a large extract. I did not measure it.
- Real supplier data, since only the pilot sample exists.

Next steps:
1. Get the segment count of the regional extract from the supplier.
2. When the extract arrives, load it and measure memory (peak RSS in the worker) and the worst-case check, such as a heavy vehicle with a closure that leaves no route.
3. If it does not fit, move to the compact structure rather than a database.

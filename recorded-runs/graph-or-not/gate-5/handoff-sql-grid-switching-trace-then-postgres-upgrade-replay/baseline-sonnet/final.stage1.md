Decision: in-process-library

Load the network into memory in a compact graph library such as igraph or rustworkx, not networkx. Keep Postgres as the source of truth.

Why the other options lose:
- recursive-sql: you already tried it with indexes on both segment ends and got 8.4 s p95 against a 1.5 s budget. The query in `sql/outage_trace.sql` carries a `path` array per row so it can detect loops. On a meshed network that enumerates paths rather than nodes, so the work grows with the number of loops. A visited-set rewrite (plain `UNION`, no path) would be cheaper, and it is worth a quick try. But each node still costs index probes inside Postgres, and I have no evidence it gets from 8.4 s to under 1.5 s.
- closure table: you measured 6.8 billion rows, and every switching operation invalidates part of it. That rules it out.
- graph database: it would add a second datastore. The grid has 2.9M nodes and 3.4M segments, which is small. Nothing in the problem needs a graph database's query language or storage.
- no-graph: this is a reachability question on a meshed network, so it needs real traversal.

Why in-memory is feasible. The networkx figure (2.1 GB for 6% of the grid, about 35 GB total) reflects networkx's per-node Python objects. It does not show that the grid is too big for memory. In a compact array-based representation, 3.4M segments are two integer arrays plus offsets. I built a synthetic graph at your size (2.9M nodes, 3.4M edges, scipy CSR). It took about 46 MB for the structure and about 370 MB peak process memory. That is a rough size check on random data, not your real topology, and it is nowhere near the 16 GB on the trace servers.

Why the other limits are not a problem:
- Regions: you don't need to split by region, because the whole grid fits in one process. That avoids the 41% of storm traces that cross regions.
- Switching feed: 45,000 device state changes a day is about one every two seconds. Each one flips a closed/open flag on one segment in the in-memory copy, with the same change written to Postgres. Rebuilding the whole structure is also an option, since building the CSR is cheap.
- Load: 900 traces an hour is one every four seconds. A single process can serve this.

How to run a trace. Start from `:source_node`, skip the opened segment and any segment that is open, and keep a visited set. Return the visited node ids, so the client's diff against normal state works unchanged. This is a plain BFS, so cost scales with the number of nodes fed, not the number of paths.

What I did not verify, and what to check before committing:
- My BFS timing was on a synthetic random graph where one trace reached every node, and it took about 2.3 s. That is the worst case and slower than real traces should be. Real feeder traces reach a subset. Measure on your real data with your storm replay.
- I have no data on how large the fed set is in a typical storm trace. If most traces reach hundreds of thousands of nodes, a pure-Python traversal may miss 1.5 s, and you would want a compiled library (igraph or rustworkx) rather than a Python loop.
- Replay last January's storm against the in-memory version and compare p95 to the 1.5 s budget. Also compare its fed sets to the SQL results on the same traces to confirm correctness.
- Decide how a trace server stays consistent with SCADA: how it loads at startup, how it applies feed updates, and what it does if it misses one. I did not design this.

I did not change any code in the repo.

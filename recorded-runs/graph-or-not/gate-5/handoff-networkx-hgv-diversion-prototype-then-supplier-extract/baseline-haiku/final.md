Decision: in-process-library

Keep the networkx prototype in `roads/diversion.py` and load the graph inside the permit worker process. A graph database or recursive SQL is not needed at 180,000 segments and 150,000 junctions.

Evidence: I timed the prototype on a synthetic network of that size, not on the real extract. Loading the graph took about 2.8 s, and each diversion query took about 0.15 to 0.3 s. That is well within a per-permit worker call. The benchmark used random topology, so connectivity was poor and most test queries found no path. The timings still reflect the work per query, which is the question here.

Caveats:
- Re-time on the real regional extract before relying on this. Real road topology and restriction density may change query cost.
- `diversion()` scans every edge to find the closed segment on each call. That is O(E) and is part of the timings above. It is fine at this size but is the first thing to index if the worker gets busier.

Where it is written down: I added the decision to the Decision bullet in `/run/work/README.md`. I found no other decision record in the work directory.

Decision: in-process-library

The recursive SQL no longer holds. I updated `docs/graph/DECISION.md`, which was `recursive-sql` at 120 ms p95. It now says `in-process-library` and keeps the old 120 ms and 640-station figures beside the new ones. That is the only file I changed. No code, indexes or dependencies were touched.

What the call turns on:
- **Latency:** 7.4 s p95 against the desk's 1 s need (the 1 s is in the earlier record), so 7.4 times over. It was 120 ms before the merge. The sections went from about 9,800 to about 389,800, which is 39.8 times, and the time went up about 62 times. The cost follows the size of the network.
- **Why the query can't be tuned:** it already uses the node-id-only `UNION` form, so there is no row-per-route waste. The indexes are in place and used. It starts from every core node, so every call has to cover the whole connected network.
- **Why cores won't help (Kofi):** there is one statement every 16 minutes or so (about 30 look-ups a day), so nothing is competing for the cores. No measurement says more cores speed up a single recursive walk. A remedy nobody has run doesn't reopen a measured failure. If you run it and it gets under 1 s p95 on the merged file, that moves this back to recursive-sql.
- **Why not a graph database:** the edge set is small for one process. On synthetic data of the same edge count, NetworkX 3.7 used about 198 MB (about 507 bytes per edge) and a plain dict about 117 MB. That is about 2.5% of the 8 GB box. The data changes only with the nightly rebuild, and a day-old answer is fine. A second store and feed would not remove the full-network walk.

What I did not measure or could not find:
- There is no copy of the real database in the repo, so the 7.4 s is your figure from the merged test file.
- The memory numbers come from random synthetic edges, not your export. The real track node count is unknown.
- I did not time the load or the search for the in-memory version. `desk.py` runs per look-up, so reloading 389,800 sections each time may cost too much. The shape I'd try is one long-running process or cached structure rebuilt after the nightly export.
- It is not known whether the national scope raises the 30 look-ups a day.

Before committing, trial it. Load the merged export, then time the search for a few dozen real closures against the 1 s p95.

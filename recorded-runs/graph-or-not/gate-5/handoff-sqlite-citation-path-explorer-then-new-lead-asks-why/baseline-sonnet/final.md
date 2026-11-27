Decision: in-process-library

We decided to run the citation-path search from a compact in-memory adjacency array, shared between the workers, and not to run the search in SQLite. SQLite stays the system of record: `citepath/refresh.py` still writes the daily snapshot there. We did not choose a graph database.

Why SQLite alone doesn't work (your suggestion, and Sanne's):
- The requirement is a search of up to 6 hops over 410M citations between 96M papers. The budget is 3 s p95 with 400 staff using it.
- The recursive query in `sql/path.sql`, with indexes in both directions, runs at 41 s p95 on a copy of the snapshot. That is about 14 times over budget. A 6-hop search on a citation graph reaches millions of papers within a few hops, and each one costs an index probe.
- A rewrite of the query might help, but nobody expects it to close a 14x gap. Nobody has measured a rewrite.
- A closure table (precomputed paths) came out at about 90 billion rows, so that route is out.

Why not the other options:
- networkx: 2.6 GB for a 20M-citation sample, so about 53 GB for the full graph, per worker. We run 6 workers on 32 GB hosts. It can't fit.
- A graph database: it could handle mid-walk filters and daily updates, but it is a new datastore to load with 410M edges, run, secure and keep in sync. It would also have to beat 3 s at this size, and we have not trialled one. Wen's array already does 0.8 s, so the evidence doesn't justify the risk and the running cost.

What the decision rests on:
- Wen's compressed numpy adjacency array fits in 6 GB and does 0.8 s, against a 3 s budget.
- Her array had two blockers. Both have a fix that keeps the design.
  1. Memory: 6 GB per worker means 36 GB across 6 workers, which doesn't fit in 32 GB. Instead write the arrays to files and open them with `mmap`, so all 6 workers share one 6 GB copy.
  2. Filters and refresh: each new filter took Wen about two weeks, and the 40-minute rebuild for the daily 1.2M new citations got a no from the platform team. To fix it, keep the year and retracted flag as separate per-paper arrays (about 300 MB) and check them during the walk. A new filter then becomes one more array and one more check. Run the 40-minute rebuild overnight from the existing refresh job and swap the files atomically. The office needs the new citations by the next morning, not within minutes, and an offline build job is much smaller for platform to operate than a service.

What is not proven yet:
- The 0.8 s figure is Wen's. It has not been reproduced here, and we don't know the mix of searches she timed (filters on or off, p95 or average, how many chains returned).
- The filter design has not been measured. A check on every edge will slow the walk somewhat, and it has to be measured against the 0.8 s.
- Still to do before committing: a load test at 400 staff with filters on, the worst-case pairs (papers that cite hub papers), and 6 workers sharing the mmap copy. Compare her chains with the SQL query's on a sample of pairs. Cap the nodes visited so a very large search ends with a clear message.

Nothing in this repo changed. `citepath/paths.py` still loads everything into networkx at worker start. It would be replaced, not tuned.

Note for the sender: I found no written decision record in the repo (the README, schema and code don't mention one). This summary is based on the earlier analysis of this question and the numbers in it. Check it against whatever Sanne and Wen actually agreed, in case anything differs.

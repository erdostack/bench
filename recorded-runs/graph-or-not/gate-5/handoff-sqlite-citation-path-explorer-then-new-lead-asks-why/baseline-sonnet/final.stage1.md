Decision: in-process-library

Build the search around Wen's compact in-memory adjacency array, and change how the filters and the daily refresh work so the two objections go away. Keep SQLite as the source of truth, and do not add a graph database.

Why not the other options:
- recursive-sql: it is at 41 s p95 against a 3 s budget, a gap of about 14 times. Indexes on both ends already exist. The query in `sql/path.sql` also unions both directions of the whole citation table into one `edge` CTE and carries a path string per row. A rewrite as a frontier-by-frontier search would help, but I would not expect it to reach 3 s. A 6-hop search on a citation graph reaches millions of papers by hop 3 or 4, and each of them costs a B-tree probe. I did not measure this, since the 410M-row snapshot isn't here. The gap to Wen's 0.8 s is a good sign that the access pattern is the problem, not a missing index.
- networkx: 53 GB per worker against 32 GB hosts with 6 workers. It cannot run.
- closure table: about 90 billion rows, so no.
- graph database: it would handle filters during the walk and incremental updates well, but it means a new datastore to load with 410M edges, run, secure and keep in sync daily. It also has to beat 3 s on 6-hop searches at 96M nodes, which I can't confirm without a trial. Wen's array already does 0.8 s, so the risk of adopting one isn't justified by the evidence.
- no-graph: shortest chains between two papers is a real traversal.

Why Wen's design is nearly there, and what to change:
1. Memory. 6 GB per copy is only a problem if each of the 6 workers holds its own copy. Write the adjacency arrays to files and open them with `mmap` (or shared memory). Then all 6 workers share one 6 GB copy in the page cache, which fits in a 32 GB host with plenty to spare.
2. Filters. The cost of two weeks per filter suggests the filters were built into the structure. Instead keep per-paper attribute arrays in node order: year (2 bytes) and retracted (1 byte) is about 300 MB for 96M papers. The walk then evaluates a predicate over those arrays for each neighbour as it goes (skip if retracted, skip if year is below X). A new filter becomes one more array and one more predicate in the walk, not a new structure. This is my proposal and I haven't tested its cost on the real data. A check per visited edge will slow the walk somewhat, and Wen should measure it against the 0.8 s.
3. Daily refresh. The office needs new citations visible by the next morning, not within minutes. A 40-minute rebuild run overnight by the existing `citepath/refresh.py` job, then an atomic swap of the files, meets that. The platform team's objection was to a service they would have to run. An offline build job that writes immutable files, plus workers that reopen them after the swap, is a much smaller thing to operate. If a nightly full rebuild still worries them, a small append-only file for the day's 1.2M citations, merged on top of the base arrays, is an option. I would start with the nightly rebuild, because it is simpler.
4. Retractions. A retraction changes one attribute value on one paper, so it fits the attribute array. It should be applied at the same nightly build.

What I did not verify, and what to check before committing:
- I have no access to the 410M-citation snapshot or to Wen's code, so I haven't reproduced the 0.8 s. Find out what mix of searches she timed. Was it with filters on? Was it p95 or an average? Did it return up to 5 chains?
- Run a load test at 400 staff: roughly measure p95 with the filters on, the worst-case pairs (papers that cite hub papers), and 6 workers sharing the mmap copy.
- Compare her results against the SQL query on a sample of pairs to confirm that the chains are the same.
- Decide what happens on a search that blows up (a very large frontier): a cap on nodes visited and a clear message in the explorer.
- Sanne's goal of staying in SQLite is mostly kept: SQLite remains the system of record and the thing `refresh.py` writes to. What changes is that searches no longer run in SQL. That is worth raising with her directly, with the 41 s versus 0.8 s figures.

I did not change any code in the repo. `citepath/paths.py` still loads everything into networkx at worker start, and it should be replaced rather than tuned.

# Graph decision

Decision: recursive-sql

The question is whether the district heating isolation screen should move the network into Neo4j, as one contractor proposes, because recursive SQL "can't cope with loops". It can: the existing walk in `sql/isolate.sql` terminates on the ring mains because `UNION` over the node id alone keeps each node once, and the measured p95 is about 35 ms against a 2 s budget. The finding it turns on is the present timing, 35 ms p95 (stated by the user; the synthetic check below gives 33 ms p95 on a network of the same size), which leaves roughly 60 times the budget.

## Workload facts

- Network: about 2,400 pipes, 1,900 nodes, 610 buildings, with ring mains and so loops (stated by the user; `db/schema.sql` comment on `pipe`)
- Isolation rate: about 40 per day (stated by the user). Total walk time at the stated p95: 40 x 35 ms = 1,400 ms per day (derived from the two figures above)
- Latency budget: under 2 s per isolation (stated by the user)
- Present timing: 35 ms p95 on the full network since the rewrite that keeps only the node id (stated by the user; not in the repo)
- Old version: hung on the rings in March (stated by the user); the walk now dedups on `node_id` with `UNION` (`sql/isolate.sql`)
- Depth needed: data-dependent; the walk continues until no new node is reached (`sql/isolate.sql`, `WITH RECURSIVE fed`)
- Edges and fan-out: 2 x 2,400 / 1,900 = 2.53 pipe ends per node on average (derived from the two figures above); tail and hubs unknown
- Required distinct set for one isolation: at most 1,900 nodes, which is the whole network (`measured`, synthetic, below)
- Engine operated today: SQLite, one file `var/heatnet.db`, exported from the asset register whenever the network changes (`README.md`); SQLite 3.53.1 on Python 3.13.18 in the measurement below
- Indexes on the walk's join columns: `pipe_a(a_node)` and `pipe_b(b_node)` (`db/schema.sql`). `EXPLAIN QUERY PLAN` shows `MULTI-INDEX OR` over both, with `SEARCH p USING INDEX pipe_a` and `pipe_b`, and no full scan of `pipe` (measured)
- Measured, synthetic network of the stated size, every pipe isolated once (`measured`, `python3 -I scratch/bench.py <work dir>`, two topologies with the same counts, scratch folder removed afterwards):
  - random topology (spanning tree plus 501 extra pipes): p50 19.0 ms, p95 32.5 ms, max 62.3 ms over 2,400 isolations; with no pipe isolated, 1,900 of 1,900 nodes reached
  - ring topology (backbone with 501 chords of length 2 to 20): p50 13.0 ms, p95 28.6 ms, max 61.7 ms over 2,400 isolations; 1,900 of 1,900 nodes reached
- Writes and freshness: the network is re-exported from the asset register whenever it changes (`README.md`); how often is unknown
- Concurrency: unknown beyond "about 40 a day"
- What was measured on the real database: nothing in the repo. `var/` and `*.db` are gitignored, so `var/heatnet.db` is not present; the 35 ms figure is the user's, not checked here
- unknown: the real network's topology and degree distribution (the synthetic topologies are not the real network); the real p95 under production load; the production plan on the real file; the owner of the 2 s budget (the control-room team, as far as the request shows); `docs/graph/CONTEXT.md` does not exist, so the engine version is taken from the repo, not a context record

## Options considered

- graph-database (a dedicated graph store, the Neo4j the contractor proposed): rejected, because the measured walk meets the 2 s budget with about 60 times headroom on the stated p95, and no measurement shows the SQL failing at this depth; adopting a server would add a second stateful system, a feed from the asset register that can drift, and a new query language, for a question at 40 a day. The contractor's premise is also contradicted by the query: the loops end because of `UNION`, as the synthetic ring topology shows (all 2,400 isolations ran to completion)
- in-process-library (the network loaded into memory and walked with a graph library): rejected, because 2,400 edges and 1,900 nodes are already walked in tens of milliseconds in SQL, and loading a copy into each process with a reload after every export adds copies and a reload step without a measured gain; no whole-network algorithm runs per request
- recursive-sql (recursive queries on the SQLite file already run): chosen, because the walk starts from the plants, is data-dependent in depth, runs against the operated database with indexed joins (`pipe_a`, `pipe_b`), and meets the budget on the stated p95 (35 ms) and on the synthetic check (33 ms p95, 62 ms max)
- no-graph (plain joins, no traversal): rejected, because which substations lose a plant depends on a walk of data-dependent depth through the pipes, not on a join that crosses a link table once

## What would change the decision

- The measured p95 of `sql/isolate.sql` on the real `var/heatnet.db` rising above 2 s (or the owner of the 2 s budget tightening it so the real p95 sits near it): first check the plan and the index use on the real file, then consider the in-process-library for a cached copy; a graph database is considered only if SQL is measured failing at the required depth after those remedies
- Isolation volume rising to many calls per second, online, with a latency budget: the arithmetic changes (statements running at once about calls per second times seconds each); this is a concurrency question for the control-room owners to set and test on the real file
- A requirement for whole-network batch results (for example, buildings lost by every pipe, ranked over all 2,400 pipes in one run): that would move this to in-process-library for the batch job, on a snapshot of the network, and not to the online screen
- Network growth to the point where the synthetic and real timings no longer agree, measured by re-running the benchmark on the real file with the same query

Nothing in the repo was changed. The only file left is this one; the synthetic benchmark folder was removed.

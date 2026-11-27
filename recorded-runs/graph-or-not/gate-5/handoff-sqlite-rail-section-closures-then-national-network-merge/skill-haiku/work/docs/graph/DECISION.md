# Graph decision

Decision: in-process-library

The question is which stations are cut off from the core network when a track section closes, now for the national network (2,600 stations, 380,000 sections from April) and not the desk's own network (640 stations, about 9,800 sections, previous decision recursive-sql). The recursive query is measured at a 7.4 s p95 on a merged test copy against a 1 s budget, so the recorded decision no longer stands; more cores were proposed but not run, and an unrun remedy does not reopen the rung. The finding that turns the answer: a section closure cuts stations off only if that section is a bridge between the core and them, so a nightly precomputation of the cut-off set per section (1.6 to 1.7 s to build on 380,000 sections here) makes each answer a lookup of 0.5 to 4 microseconds, which fits the 1 s budget; a graph database is not needed because the network fits in one process and changes once a night.

## Workload facts

- Stations: 2,600 (stated by the user, national network from April); previously 640 (`db/schema.sql` `station`; previous record)
- Track sections: 380,000 (stated by the user, same nightly export); previously about 9,800 (previous record). Usable in both directions (`db/schema.sql` `section`)
- Track nodes: count not stated and not in the repo, for either network (`db/schema.sql` `track_node`). Previous synthetic checks used 3,000 and 8,000 nodes; the national checks below use 150,000 and 300,000 nodes, which are assumed, not stated
- Core nodes: marked by `track_node.is_core = 1`; count not stated for either network. The national checks use 0.2 percent of nodes as core
- Question asked of the connections: stations with no track node reachable from any core node with one section removed. Previously a recursive walk from the core set (`sql/cut_off.sql`, `WITH RECURSIVE reach`); now a bridge question on the same graph (a section cuts stations off only if it is a bridge between the core and them)
- Load: about 30 closures per day (stated by the user; previous record). No national load figure was given: unknown
- Latency budget: 1 s per answer (stated by the user; previous record)
- Present timing on the desk's own network: 120 ms p95 (stated by the user; previous record; the repo holds no timing)
- Present timing on the national network: 7.4 s p95 for the cut-off query on a merged test file, with indexes on both section ends and a plan showing index lookups (stated by the user; measured on a copy, not re-run here). This is the measurement that moves the decision
- Remedy proposed: more cores on the box (stated by the user, Kofi). Not measured in this check. SQLite runs one statement on one thread, so more cores are not expected to shorten one query; unverified here
- Freshness: the register export is rebuilt every night (stated by the user; `README.md`), so answers reflect the previous night's network. The new structure can be rebuilt on the same schedule
- Box: one machine with 8 GB (stated by the user; previous record)
- Engine operated today: SQLite, `var/infra.db` (`README.md`). No national file is in the repo
- Indexes on the walk's join columns: `section_a(a_node)` and `section_b(b_node)` (`db/schema.sql`)
- Measured earlier, desk network, synthetic (previous record; `python3 -I scratch/bench.py <work dir>`, scratch folder removed afterwards): 3,000 track nodes gave p95 116.0 ms, 8,000 gave p95 319.9 ms, both with 9,800 sections and 640 stations
- Measured now, national scale, synthetic (in-memory, Python 3.13, this machine; random topology, 380,000 sections, 2,600 stations, 60 random closures per run for the walk and 200 for the lookup):
  - Plain per-closure walk over the adjacency lists (no SQL, one search over the whole network per closure): 150,000 nodes gave p50 976 ms, p95 1,109 ms, max 1,355 ms; 300,000 nodes gave p50 899 ms, p95 1,253 ms, max 1,401 ms. Against a 1 s budget this is at or over the line, so the bare in-memory walk does not hold on its own
  - Precomputed cut-off set per section (bridge analysis once per snapshot, then a lookup by section id): 150,000 nodes gave a build of 1.71 s, 2,537 bridges, lookup p50 0.5 microseconds, p95 0.9 microseconds, max 10.7 microseconds; 300,000 nodes gave a build of 1.61 s, 84,953 bridges, lookup p50 0.6 microseconds, p95 4.3 microseconds, max 16.8 microseconds
  - Correctness of the precomputed lookup: checked against a brute-force walk on 300 small random graphs (5 to 60 nodes, parallel sections, disconnected parts, several core nodes), 13,838 single-section closures, 0 mismatches; and on three random closures at each national size, 0 mismatches
  - Memory, national synthetic: process peak about 166 MB (150,000 nodes) and about 250 MB (300,000 nodes) with the adjacency lists built, measured with the process's maximum resident size; well inside the 8 GB box. The structure is one copy per process
- Measured on the real file: nothing in the repo. The 7.4 s p95 is the user's figure on a merged test file, not a run here
- Writes: the nightly rebuild is the only write (`README.md`); no write happens at query time
- unknown: the real track node count and the number of core nodes for the national network; the real topology (synthetic graphs are random; real rail networks have more branch lines, so more bridges, which the precomputed structure handles but the build time has not been measured on); the nightly export window and how long the rebuild can take; whether closures are ever requested for two sections at once (the bridge lookup covers one closed section); the closure rate at national peak; whether more than one process will hold the structure; the owner of the 1 s budget (the desk, as far as the request shows)
- `docs/graph/CONTEXT.md` does not exist in the repo

## Options considered

- graph-database (a dedicated graph store, the one Ravi proposed; no product named): rejected, because the national network is 380,000 sections, which fits in one process (about 250 MB measured peak here on an 8 GB box), and it changes once a night, so the criteria for a store (an edge set too large or changing too fast for a copy per process, with SQL measured failing) do not hold; a server would add backup, upgrade and a second copy fed from the nightly export, for about 30 closures a day
- in-process-library (the network loaded into memory and answered from a structure built once per nightly snapshot): chosen, because the national network fits in one process, the per-closure answer is a lookup of under 20 microseconds after a build of about 1.7 s, and the lookup is checked against the brute-force walk. Conditional on a trial on the merged file, as listed below. A plain in-memory walk per closure is not chosen, since it measured p95 1.1 to 1.25 s here
- recursive-sql (recursive queries on the SQLite export already run): rejected, because it is measured failing at the national scale: 7.4 s p95 on a merged copy against a 1 s budget, with the index remedy already in place (the plan shows index lookups). The proposed cores remedy has not been run and does not reopen the rung
- no-graph (plain joins, no traversal): rejected, because which stations are cut off depends on paths through sections of data-dependent length, and whether a section is a bridge is a whole-network property, not a join across a link table

## What would change the decision

- The trial on the merged file fails: the nightly build of the cut-off structure exceeds the export window, the lookup p95 is over 1 s, or the process holds more than the box can spare with the other desk processes. Then the next step is a measured run of the proposed cores change on the merged file; graph-database is considered only if that and the in-process build both fail
- Answers needed during the day, on the live register rather than the previous night's export: the precomputed structure would need an update after each change, which is a freshness change; if changes are frequent, that would move this toward graph-database, measured on the real change rate
- Requests for two or more sections closed at once: the bridge lookup covers one closed section. A combined closure needs its own answer, measured on the real file; if it runs per request, the bare walk (about 1 s here) would be the cost and the budget would need the owner's review
- Closures rising to many per minute at peak, so that calls overlap: a concurrency question for the desk to set and test on the real file
- A requirement to rank or score all sections at once (for example, every section's station impact in one batch): that is a whole-graph job, which fits this option on a snapshot

Changed by this review: the Decision line (from recursive-sql), the workload facts for the national network, and the options. The desk-network figures from the previous record are kept beside the new ones. `sql/cut_off.sql` and the rest of the repo are unchanged; the synthetic national checks were run in memory with no files written.

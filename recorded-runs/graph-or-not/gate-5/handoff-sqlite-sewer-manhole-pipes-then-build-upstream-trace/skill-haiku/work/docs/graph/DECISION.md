# Graph decision

Decision: recursive-sql

The desk asks which sewers drain into a flooded manhole, stopping at pumping stations, and the asset data lead asks whether the network belongs in a graph database. The answer is recursive SQL on the SQLite export the desk already reads: the walk is a variable-depth upstream traversal over 15,100 pipes, which is a real traversal, but the edge set is small, indexed and already in SQLite, and a measured walk takes milliseconds. The draft in `sql/upstream_draft.sql` never finishes because it carries a hop count through the recursion while overflow links are digitised in both directions, which creates cycles; that is a query bug, not a storage limit.

## Workload facts

- Nodes: 14,200 in the export (stated by the user).
- Pipes: 15,100 in the export (stated by the user); 15,100 / 14,200 = 1.06 pipes per node, so average upstream fan-out is about 1.06 (derived from the two stated counts).
- Export refresh: monthly, as a SQLite file at `var/drainage.db`, not committed (`README.md`, `.gitignore`, stated by the user).
- Load: about 15 floods a week, roughly two per day, one walk per flood, run from a laptop (stated by the user).
- Question asked of the connections: upstream of one node, walking backward along `pipe.ds_node` to `pipe.us_node` to a depth the data decides, stopping at pumping stations (stated by the user; query text in `sql/upstream_draft.sql`). This is a walk from one starting point, not a one-step link lookup and not a whole-graph algorithm.
- Stop rule: do not list a pumping station or anything that drains into it (stated by the user, network ops lead). The draft does not apply this rule.
- Cycles: overflow pipes are digitised once per direction where water runs both ways (`db/schema.sql`, comment on `pipe`), so the directed graph has two-node cycles by design. The draft's recursive part carries `hops` and uses `UNION`; rows that differ in `hops` are not duplicates, so the recursion does not terminate on a cycle.
- Measured, non-termination: on a 5-node scratch SQLite graph (a 2-cycle between nodes 2 and 3) the draft query was interrupted by a progress handler after 2,000 callbacks (about 0.14 s). Run with SQLite 3.53.1 under Python 3.13, on the toy graph built in this run. The Eastgate export was not available, so this is not measured on Eastgate.
- Measured, fixed walk: the same toy graph, with the recursive step carrying `node_id` only (`UNION`) and excluding pumping stations from the recursive step, returned the correct upstream sets (from node 2: 1, 3, 5; from node 3: 1, 2, 5; node 4, a pumping station, excluded). Run with SQLite 3.53.1 under Python 3.13. The query plan showed `SEARCH p USING INDEX pipe_ds (ds_node=?)` inside the recursive step, so the walk uses the existing index.
- Measured, timing at the stated size: a synthetic network of 14,200 nodes and 15,100 pipes (random tree-like links plus overflow pairs, pumping stations on 120 nodes, seed 7; not the Eastgate topology), 50 random start nodes, node-only walk with the pumping-station stop, same SQLite: median 0.01 ms, maximum 41 ms, largest upstream set 10,178 nodes. Synthetic topology, so it shows the order of magnitude only.
- Measured, memory for an in-process copy: a dict-of-lists adjacency of the 15,100 synthetic pipes measured 1,082 KB traced by `tracemalloc`, about 73 bytes per edge (Python 3.13). At the stated edge count that is about 1.1 MB per process; the monthly reload is a single file read.
- Arithmetic: the upstream set of any node is at most 14,200 nodes, so a walk touches at most 15,100 pipe rows through the `pipe_ds` index. At about 15 walks a week, load is negligible.
- Indexes in place: `pipe_ds` on `pipe(ds_node)` and `pipe_us` on `pipe(us_node)` (`db/schema.sql`).
- Stack: Python 3.12, standard library only (`README.md`). The measurements above ran on Python 3.13 and SQLite 3.53.1 (`sqlite3` in the standard library); the desk's Python 3.12 and its SQLite version are not recorded in the repo, so they were not checked.
- Graph-database test: no measurement of any graph database was run here; `references/engines.md` lists Neo4j and LadybugDB as documentation only.
- unknown: the Eastgate subgraph itself (how many overflow pairs, the depth of its deepest walk, whether any pumping station sits upstream of a manhole in practice); the real flood-time latency budget (not stated); whether the desk needs hop counts, which the node-only walk does not return; whether a flooded node may itself be a pumping station (the stop rule then leaves an empty list); whether the export holds more rows than the stated counts. Looked in: `README.md`, `db/schema.sql`, `drainage/desk.py`, `drainage/__init__.py`, `sql/upstream_draft.sql`, `.gitignore`. `var/drainage.db` is not in the repo and was not available.

## Options considered

- graph-database (a dedicated graph store): rejected, because the walk runs over 15,100 pipes in an export refreshed monthly, the largest measured walk at that size took 41 ms, and no deep online traversal over an edge set too large for one copy was shown. Adopting one would add a second stateful system and a feed from the asset export for no measured gain.
- in-process-library (the edges loaded into memory): holds on size (about 1.1 MB per process, 73 bytes per edge measured), but not chosen, because the recursive SQL rung already holds and the data already sits in the SQLite file the desk reads; adopting a library would add a loader and a second copy to keep in step with the monthly export.
- recursive-sql (recursive queries on the database already run): chosen, because the walk starts from one node, SQLite is already operated, the indexes exist, and the measured walk is fast. The fix is to drop the `hops` column from the recursion, keep `UNION` on `node_id`, and add the pumping-station exclusion to the recursive step, as in the toy test above. This is a remedy that has been run only on the toy graph and the synthetic network, so it has to pass on the real export before the desk relies on it.
- no-graph (plain joins, no traversal): rejected, because the upstream list depends on the depth the data reaches, which a single join cannot give.

## What would change the decision

- A measured walk on the real Eastgate export, or any catchment, that exceeds the latency budget the desk sets (the budget is not stated in the repo; the desk's lead owns it) after the fixed query has run would move this to in-process-library, for batch precomputation, or to graph-database only if the same walks must run online at many times the current rate.
- A requirement for hop counts or distances that the node-only walk cannot meet, if it cannot be met in SQL with the cycle guard, would move this to in-process-library, where a breadth-first search over the loaded edges gives them directly.
- Edge count or fan-out at the tail rising far above the stated 15,100 pipes and 1.06 pipes per node, so that the largest upstream set approaches the full network on every flood, would move this to in-process-library.
- A need for many concurrent walks from a service, rather than about 15 a week from one laptop, would move this to graph-database; the owner of that load figure is the desk and the asset data lead.

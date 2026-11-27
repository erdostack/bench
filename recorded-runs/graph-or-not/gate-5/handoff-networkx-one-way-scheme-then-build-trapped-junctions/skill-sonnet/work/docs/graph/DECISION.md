# Graph decision

Decision: in-process-library

The question: fix the trapped-junctions check so it follows the traffic team's rule (a road junction is trapped if you cannot drive from it to the ring road, or cannot drive to it from the ring road, footpaths ignored), and whether to load drafts into a graph database. The answer is a graph library in the script: this is a whole-graph reachability pass, in both directions, over about 1,450 junctions and 1,900 segments, run as a batch on a laptop. networkx is already installed on the planners' machines and a correct run took under a second on a synthetic draft of that size.

## Workload facts

- The question asked of the connections: for every non-ring junction, can the ring road be reached, and can it be reached from the ring, along directed road segments. oneway/trapped.py does a breadth-first search per junction, outbound only, and stops at MAX_STEPS = 25; it reads every segment regardless of mode (oneway/trapped.py, db/schema.sql).
- Where the current code differs from the rule, which is the actual cause of the planners' distrust: it gives up after 25 steps, so junctions on the long one-way market loop are flagged (stated by the user: 63 flagged on last week's draft, most on that loop); it never checks the inbound direction; and it ignores the mode column, so footpath segments ('foot') are used as roads, and junctions only on footpaths are not excluded (oneway/trapped.py, db/schema.sql, rule stated by the user).
- Depth: data-dependent; the market loop alone is longer than the 25 steps the code allows. No depth limit is wanted by the business (stated by the user).
- Size: about 1,450 junctions and 1,900 segments per draft (stated by the user). Edges as directed moves: up to 2 x 1,900 = 3,800, from the oneway codes 0 (both ways), 1 and -1 (derived from db/schema.sql).
- Load: two planners run 20 or 30 drafts a week on their laptops (stated by the user), a batch job, no latency budget stated, one process each; there are no concurrent users and the draft file is a snapshot exported from the sketch tool (README.md).
- What is operated: each draft is its own SQLite file var/<draft>.db, not committed; there is no database server (README.md).
- Ring road: junction.on_ring = 1, "two-way all round" (db/schema.sql).
- Measured: on a synthetic draft with 1,450 junctions, 1,900 segments and 60 ring junctions, built with the repo's schema, a networkx DiGraph built from road segments only and queried with descendants and ancestors of the ring set took 0.86 s and 1.5 MB peak Python memory (measured, networkx 3.7, Python 3.13, tracemalloc). The existing function took 0.02 s on the same data, because it gives up early, not because it is right. Random data, so only the order of magnitude is shown. 30 drafts a week x 0.9 s is about 27 s of work a week (derived).
- Drafts are rebuilt per run from the file, so freshness is not an issue: a reload per run is the load.
- unknown: how many junctions are reachable only over footpaths in real drafts and whether the ring road is a single connected component; the real drafts are not in the repo. unknown: whether the sketch tool can export a draft that does not have the mode column filled correctly.

## Options considered

- graph-database (the dedicated store the transport modelling consultant suggests): rejected, because each draft is about 3,800 directed moves in a file one planner loads on a laptop, used 20 to 30 times a week; a server would add a second store and a load step with no online traffic to serve.
- in-process-library (the edges loaded into memory, networkx, already installed on the planners' machines): chosen, because the job is a whole-graph reachability pass over a snapshot of about 3,800 directed moves, which measured 0.86 s and 1.5 MB, and it is the usual shape of a batch analysis on a laptop. Shape of the fix (not applied here): build a directed graph from segments where mode = 'road' only, with oneway 0 as two edges, 1 as a to b and -1 as b to a; take the junctions that touch at least one road segment; compute everything reachable from the ring set and everything that can reach the ring set once each, in a single multi-source pass per direction, with no step cap; report the non-ring road junctions that are missing from either set.
- recursive-sql (recursive queries on the draft's SQLite file): rejected, because the question is a pass over every junction in two directions on a snapshot file, not a walk from one starting point in an operated database, and the directed moves would first need a derived view of both orientations of every segment; no measurement shows it is simpler or needed, and the in-process pass already meets the need.
- no-graph (plain joins, no traversal): rejected, because reachability to the ring has a depth that depends on the data (the market loop is longer than 25 steps), so it cannot be written as joins that cross a table once.

## What would change the decision

- A draft file of a size where the in-memory pass takes minutes or does not fit a laptop (the edge count against the planners' memory; it is about 3,800 moves now) would move this to graph-database, or first to a leaner in-process structure; the repo sets no limit, so the traffic team owns what run time is acceptable.
- Planners wanting a shared, always-on service that answers interactively for many users at once over a continuously edited network would move this toward graph-database; nothing in the request says that.
- If networkx stops being installed on the planners' machines, the same pass can be written by hand as a breadth-first search over a dict, with no change to the decision.

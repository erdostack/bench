# Graph decision

Decision: in-process-library

The society asked whether its "circles" exhibit page, which steps from one woman through shared events out to the whole network, needs Neo4j, an in-memory graph library, recursive SQL or no graph at all. The network is 18 women and 139 pairs who share an event, loaded from a CSV that never changes, so the whole graph fits in memory and a library walks it in a few steps. The finding it turns on: from any one of the 18 women, every other woman is reached within 2 steps (measured from the repository's CSV).

## Workload facts

- 18 women, 14 events, 89 attendances; the study's own data that will never change (stated by the user)
- The pages run on the society's small shared web host, a few dozen visitors a week (stated by the user)
- A board member proposed Neo4j because "it's a social network" (stated by the user; a proposal, not a measurement)
- The data is `data/attendance.csv` with one row per woman and event; `society/data.py` reads it, and `load_attendance()` is called on each request (`data/attendance.csv`, `society/data.py`, `society/pages.py`)
- Counted from the CSV: 89 rows, 18 women, 14 events (`measured`: stdlib script reading the CSV; nothing written to disk)
- Derived: women-to-women pairs that share at least one event, as an undirected count = 139 (measured from the CSV; the 89 attendances across 14 events give the edges)
- Measured: a breadth-first walk from each of the 18 women over shared-event links reached all 18 women from every start; the deepest layer was 2 steps (for example Brenda Rogers: 1 + 15 + 2 by layer; Evelyn Jefferson: 1 + 17). The circles page's "step by step out to the whole network" therefore stops at step 2 for this data (`measured`: stdlib BFS over the CSV; nothing written to disk)
- networkx 3.7 is pinned in `requirements.txt`
- No database is in the repository and none is operated for the site; the repo has no SQL schema or connection (repository file listing)
- `society/pages.py` has the TODO for the circles page; nothing in it yet walks a graph (`society/pages.py`)
- unknown: the host's Python version, memory limit and whether it can run a database server; the repo does not say
- unknown: whether the exhibit wants more than the first two layers; the data does not reach beyond 2 steps

## Options considered

- graph-database (a dedicated graph store such as Neo4j, as the board member proposed): rejected, because the graph is 18 nodes and 139 pairs, it never changes, and the site gets a few dozen visitors a week. A server would be a second stateful system to deploy and keep running on a small shared host, and the data would be copied into it, for no gain. The "it's a social network" framing does not change the size of the walk.
- in-process-library (the edges held in memory with networkx, which is already pinned, or a plain adjacency dictionary and breadth-first loop): chosen, because the whole graph is 139 pairs and fits in memory with room to spare, the data is static so no reload is needed, and the walk is at most 2 steps from any start (see the measured figures).
- recursive-sql (recursive queries on a SQL database): rejected, because no SQL database is operated for this site and the repository has none; adding one only for an 18-node static graph would be a new store, not a reuse. The rule that a shallow walk stays where the edges already live does not apply, since they live in a CSV.
- no-graph (plain joins, no traversal): rejected, because the page follows the shared-event link more than one step, to the whole network; a single join gives only the first layer of direct connections (for example, Brenda Rogers's 15 direct connections), not the layers that follow.

## What would change the decision

- The data grows to a size or churn where a copy in each process no longer fits or needs frequent reloads, for example attendance records added continuously; this would be measured on the real file before any change.
- The site already has a SQL database operated for other pages; in that case recursive SQL over the existing tables would be the cheaper option for the same 2-step walk, and the decision would move to recursive-sql.
- The exhibit or the study requires a walk to a depth the data does not reach today, or a live feed from another system; this would be re-examined on the real data.
- A graph-database move is not supported by any condition in the current evidence; it would only be reconsidered if the scale and update pattern above were both met.

Decision: recursive-sql

Keep the sewer network in the SQLite export and do the upstream walk there with a recursive query. Do not adopt a graph database for this; 15,100 pipes refreshed monthly is well within what SQLite walks in milliseconds.

The draft in sql/upstream_draft.sql never finishes on Eastgate because it carries a hop count through the recursion, and the overflow links are digitised in both directions, so the walk loops forever. Fix: keep UNION on node_id only (drop hops), and add a join on node so that pumping stations are neither returned nor expanded. I ran this on a toy graph with a two-node overflow cycle and it returned the right upstream sets; it has not been run on the real Eastgate export, so check it there before relying on it.

Numbers this rests on: a synthetic network at the stated size (14,200 nodes, 15,100 pipes) gave a median upstream walk of 0.01 ms and a maximum of 41 ms, on SQLite 3.53.1. The synthetic topology is not Eastgate's. An in-process copy would be about 1.1 MB per process, so the library option would also fit, but the recursive-SQL option already holds and avoids a second copy of the data.

Not measured or not known: the Eastgate subgraph itself, the desk's latency budget, whether the desk needs hop counts, and what happens when the flooded node is a pumping station (the report would be empty).

Nothing in the repo was changed except the new file docs/graph/DECISION.md.

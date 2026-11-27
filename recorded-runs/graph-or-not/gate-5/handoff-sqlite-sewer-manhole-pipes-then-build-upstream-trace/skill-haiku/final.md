I wrote `drainage/upstream.py` with `upstream_manholes(conn, node_id)`. It returns the sorted node ids that drain into `node_id`, not including the node itself.

It is the recursive SQL the record chose (recursive-sql), with the fix the record describes. The walk carries only `node_id` and uses `UNION`, so the overflow pipes that run both ways do not loop it. Pumping stations are never listed and never walked through, so anything that drains only through one is left out too. If the flooded node is itself a pumping station, the list is empty.

Checked on a small in-memory copy of `db/schema.sql`, including a two-node overflow cycle, a pumping station with a rising main, an outfall and an absent node. Results matched the rule by hand. I did not run it on the real export, which is not in the repo, and the walk timing in the record comes from a synthetic network.

Things to decide:
- The function lists every non-pumping-station node that drains in, not only `manhole` nodes. The name says manholes, but the request said node ids. Say if the desk wants the filter added.
- `desk.py` still has its TODO. I did not wire the call in, since you said the desk would call it.
- The record leaves open whether the desk needs hop counts. This list does not return them.

Nothing else in the repository was changed; `docs/graph/DECISION.md` was not edited.

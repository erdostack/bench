I wrote `drainage/upstream.py` with `upstream_manholes(conn, node_id)`. I didn't edit `drainage/desk.py`, so its TODO is still there for you to wire up.

It follows `docs/graph/DECISION.md` (recursive-sql on the existing SQLite export). It is one recursive query that walks `pipe` from `ds_node` back to `us_node`, and it returns the sorted list of node ids that drain into `node_id`, not the node itself.
- **Loops:** it deduplicates on node id alone, with no hop counter. This is the fix the record gives for the draft in `sql/upstream_draft.sql`, which never finishes on the two-way Eastgate overflow links.
- **Pumping stations:** the walk never steps onto a node with `kind = 'pumping_station'`. The station is not listed and nothing is traced through it, so its catchment is left out.

I checked it on a small in-memory database built from `db/schema.sql`. It covered a two-way overflow pair (it terminates), a station on the route (not listed), a node upstream of a station that also drains by another route (still listed), a node with no upstream (empty list) and an id that doesn't exist (empty list). I haven't timed it on the real export, because there is none in the repo. The record's evidence is the bound of at most 14,200 nodes and 15,100 pipes per trace, with both pipe columns indexed.

Two readings of the rule are mine, and each is easy to change:
- **Other routes:** a manhole is dropped only if every route from it to the flooded node goes through a station. The decision record lists this as a rule to confirm with the network ops lead. If the intended rule is to drop anything that also drains into a station, the query changes.
- **Flooded node is a station:** if the flooded node is itself a pumping station, the walk starts from it anyway, and it returns what drains into it up to the next station.

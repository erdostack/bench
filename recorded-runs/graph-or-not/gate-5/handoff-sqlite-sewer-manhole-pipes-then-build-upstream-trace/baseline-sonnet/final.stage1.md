Decision: recursive-sql

Stay on the existing SQLite export and do the trace with a recursive query. This isn't a case for a graph database or an in-memory graph library. The data is small (about 14,200 nodes and 15,100 pipes), it refreshes monthly, and the desk makes about 15 lookups a week from a laptop. The `pipe_ds` and `pipe_us` indexes are already in `db/schema.sql`. A graph database would add a second system to load and sync for 15 queries a week. A graph library would add a dependency, and the README says standard library only.

**Why the draft never finished on Eastgate**
- The overflow links run both ways there, so the network has cycles.
- The draft carried `hops` in the CTE columns. `UNION` only removes duplicate rows, and a revisit with a larger `hops` counts as a new row, so the walk never ended.
- The new query keeps only `node_id` in the CTE. A node already reached is never expanded again, so loops end.
- The draft's per-node hop count is dropped as a result. The desk output is sorted by asset ref instead.

**Pumping stations**
- The recursive step refuses to step onto a node of kind `pumping_station`. The station isn't listed and the trace doesn't go through it, so anything reached only via the station is left out.
- A node upstream of the station that also drains into the flooded manhole by another route will still be listed. It does drain there directly, so I read your rule as "don't go through the station". Tell me if the ops lead means something stricter.
- If the flooded node is itself a pumping station, the result is empty, since that catchment belongs to the pumping team.
- Rising mains are not special-cased. They start at a pumping station, so the trace stops there.

**Changes**
- Added `drainage/upstream.py` with `upstream_manholes(conn, node_id)`. It is standard library only.
- Wired it into `drainage/desk.py` in place of the TODO. The report now prints a count and one line per node: asset ref, kind and catchment.
- I left `sql/upstream_draft.sql` as it was. You can delete it now.

**Testing**
- There is no `var/drainage.db` here, so I could only test on a small in-memory database built from `db/schema.sql`.
- That test had a two-way overflow loop, a cross-catchment link, and a pumping station with a manhole behind it. The query finished, listed the right nodes, and left out the station and what's behind it.
- I haven't run it on the real export or timed it. At this size I expect it to be fast, but I couldn't confirm that.
- I didn't add a test file.

**When to revisit**
Look again at a graph database or library if the desk starts running thousands of traces, or needs path or flow analysis that SQL handles badly. Nothing in the request suggests that.

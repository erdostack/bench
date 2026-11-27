`nearest_depot(conn, junction_id)` in `recovery/nearest.py` now returns `(depot_id, minutes)`, or `None` if no depot can reach the junction. Before, it returned only the depot id.

How it works:
- **Route times:** it still builds the road graph from `segment` with bus-gate segments left out, because the 26-tonne truck can't use them. When two segments join the same junctions it keeps the quicker one.
- **Search:** it now does one shortest-path search from the breakdown junction and reads off each depot's time. The old version ran a separate search per depot. Roads are two-way, so the times come out the same.
- **Ties:** if two depots take the same time, the lowest `depot_id` wins. This is the same as before.
- **Depot on the junction:** a depot sitting on the breakdown junction returns `0` minutes.
- **Unknown junction:** a junction that doesn't exist, or whose only roads are bus gates, returns `None`. The exception is a junction that has a depot standing on it, which still returns `(depot_id, 0)`.

I checked it by hand on a small in-memory SQLite database built from `db/schema.sql`. The cases were a bus gate beside a slower road, parallel segments, a depot on the junction, an unreachable junction and an unknown id. There is no `var/roads.db` or test suite in the repo, so I haven't run it against real data.

Any caller that expects a bare depot id will now get a tuple. I found no other callers in this repo.

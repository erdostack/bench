I rewrote `nearest_depot(conn, junction_id)` in `recovery/nearest.py`. It now returns `(depot_id, minutes)` for the depot with the least driving time to the junction, or `None` if no depot can reach it.

The old code counted hops, not minutes, and `load()` kept only the last row when two segments joined the same pair. So a bus-gate row could replace the legal road. The fix does three things:

- Path cost is `minutes`.
- Bus-gate segments (`bus_gate = 1`) are left out, since a 26-tonne lorry may not use them. This comes from the decision record in `docs/graph/DECISION.md`, not from your request. If that rule is wrong, tell me.
- Where two segments join the same pair, the shorter time is kept.

Ties go to the lower `depot_id`, as before. A depot on the breakdown junction itself returns `0.0` minutes. Previously that case was skipped because the junction was missing from the graph. This is a change too, so say if you want it reverted.

I checked this on a small in-memory SQLite network built from `db/schema.sql`. It picked the 5-minute depot over the 32-minute one, ignored the bus-gate shortcut, returned `None` for an unknown junction, and returned `0.0` for a depot on the breakdown junction. I did not run it against the real `var/roads.db`, which is not in the repo. `load()` is only called from `nearest_depot`, so its changed behaviour affects nothing else here.

Nothing outside `recovery/nearest.py` was changed, and `docs/graph/DECISION.md` was not edited.

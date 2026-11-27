`cut_off(conn, down_station)` is now in `linewatch/shutdown.py`. It returns the sorted ids of the stations that would be cut off while `down_station` is out, not counting `down_station` itself.

It is a thin wrapper over `cut_off_by_shutdown`, which was already in the file and does the actual work. I didn't duplicate the logic, so the two can't disagree.

- **Flow rules:** a station is cut off when it has no directed conveyor path to any dock. Stations are `kind = 'station'`. Docks are never reported.
- **Bypass segments:** these are hand-operated and ignored, as in the existing code.
- **Already cut off:** a station that already has no path to a dock before the shutdown is not reported. For example, two stations that only feed each other in a loop never appear. The result is what the shutdown changes. If you want everything with no route to a dock while `down_station` is out, regardless of before, say so. It is a one-line change.
- **Down station is a dock:** its docks are removed too, so stations whose only way out was that dock are reported.
- **Unknown station:** if `down_station` isn't a station id it raises `KeyError`. Without that check, networkx would have raised its own less clear error.

I checked it by hand on a small in-memory SQLite database built from `db/schema.sql`. The cases were a chain, a join, a bypass that doesn't count, a dock going down, a loop that was already cut off, and an unknown id. There is no `var/layout.db` or test suite in the repo, so I haven't run it on the real layout and didn't add tests. `linewatch/reach.py` is untouched; it treats segments as undirected, which isn't right for this check.

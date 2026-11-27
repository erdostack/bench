# permit-diversions

Checks a diversion for an abnormal-load or heavy goods permit when a road segment is closed: the quickest way
round the closure for that vehicle.

- Road data: `var/roads.db` (SQLite, not committed; tables in `db/schema.sql`). Today it holds the county sample
  the supplier sent for the pilot; the full extract replaces it when it is delivered.
- `roads/diversion.py`: the prototype, networkx.
- Runs as a worker on the permit platform.

## Storage decision

In-process library (networkx in the worker); no graph database, no recursive SQL. Decided for the supplier's
regional extract of 180,000 segments and 150,000 junctions: about 285 MB for the graph on a synthetic network
of that size (limit 1.5 GB). Revisit if an extract grows past roughly 600,000 segments, and measure the
worst-case check (a closure with a long or no detour, which searches the whole network) against the 2 s limit
on the real extract before go-live.

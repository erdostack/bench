# permit-diversions

Checks a diversion for an abnormal-load or heavy goods permit when a road segment is closed: the quickest way
round the closure for that vehicle.

- Road data: `var/roads.db` (SQLite, not committed; tables in `db/schema.sql`). Today it holds the county sample
  the supplier sent for the pilot; the full extract replaces it when it is delivered.
- `roads/diversion.py`: the prototype, networkx.
- Decision (full regional extract, 180,000 segments and 150,000 junctions): in-process library. Keep networkx and load the graph per worker process; a graph database and recursive SQL are not needed at this scale. Timed on a synthetic network of that size (load about 3 s, one diversion query about 0.2 to 0.3 s). Re-time on the real extract before relying on it.
- Runs as a worker on the permit platform.

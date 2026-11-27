# permit-diversions

Checks a diversion for an abnormal-load or heavy goods permit when a road segment is closed: the quickest way
round the closure for that vehicle.

- Road data: `var/roads.db` (SQLite, not committed; tables in `db/schema.sql`). Today it holds the county sample
  the supplier sent for the pilot; the full extract replaces it when it is delivered.
- `roads/diversion.py`: the prototype, networkx.
- Runs as a worker on the permit platform.

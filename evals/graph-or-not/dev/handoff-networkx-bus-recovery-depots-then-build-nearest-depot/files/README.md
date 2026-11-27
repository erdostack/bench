# bus-recovery

Control-room helper: when a bus breaks down, which depot sends the recovery truck. The road network the
control room uses is exported to `var/roads.db` (SQLite, not committed; tables in `db/schema.sql`).

- `recovery/nearest.py`: nearest_depot(conn, junction_id).
- Python 3.12 with networkx (already used by the control-room app).

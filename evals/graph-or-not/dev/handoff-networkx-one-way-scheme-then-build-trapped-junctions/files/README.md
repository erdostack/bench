# oneway-scheme

Checks for the old-town one-way street consultation. Each draft scheme is a SQLite file, `var/<draft>.db` (not
committed; tables in `db/schema.sql`), exported from the traffic team's sketch tool.

- `python -m oneway.report var/<draft>.db` prints the junctions the draft traps.
- Python 3.12; networkx is installed on the planners' machines.

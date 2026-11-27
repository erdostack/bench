# plantgraph

Outside-plant graph for route planning: sites (exchanges, cabinets, chambers), the cables between them, and
`adjacency`, the edge list the route planner walks.

- `db/schema.sql`: tables.
- `jobs/build_adjacency.py <db> [--from-batch N]`: adds one `adjacency` row (origin `cable`) per in-service cable.
- `var/plant.db`: local working copy.

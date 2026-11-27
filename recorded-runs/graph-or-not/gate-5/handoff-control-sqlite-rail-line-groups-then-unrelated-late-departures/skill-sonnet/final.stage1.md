Decision: in-process-library

Load the line-station rows into memory and take connected components with networkx; do not adopt a graph database. Grouping 140 lines that connect directly or through other lines is a whole-graph connected-components job. The input is about 2,300 rows (the numbers you gave), which is 2,300 / 1,100 stations, or about 2.1 lines per station, and it runs once a month. A graph database would be a second store to run and feed for a monthly batch.

Why not the others: a single join cannot follow "through other lines" (no-graph), and recursive SQL fits a walk from one start, so labelling every line takes more code than the library for no gain.

How to do it in netmap/groups.py (not applied; I only wrote docs/graph/DECISION.md):
- Read `SELECT line_id, station_code FROM line_station`.
- Build a graph with an edge from each line to each of its stations, take `nx.connected_components`, and keep only the line nodes. Plain union-find works too if networkx is not a declared dependency (it is installed here, but README.md does not list it).
- Return `{line_id: family_number}` with families numbered in a fixed order, for example by smallest line_id, so the colours do not shift from month to month.

Not found: var/rail.db is not in the repo, so I measured nothing; the sizes are yours. Nothing else in the repo was changed.

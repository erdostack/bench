Decision: in-process-library

Load line_station (about 2,300 rows) into memory and group lines by connected components. Two lines are in the same family if they share a station, and transitively through other lines. Each component becomes one colour family. A plain-Python union-find over the station codes does this in a few lines with no new dependency. networkx's connected_components on a line-station bipartite graph is equally correct if the team prefers a library.

Why:
- The problem is a traversal (connected components), so "no-graph" is wrong. But the size is tiny: 140 lines, 1,100 stations, about 2,300 line-station rows, rebuilt once a month. Nothing here needs a dedicated graph database, and the vendor-style pitch that a graph database is the natural first use does not hold at this scale.
- Recursive SQL could compute components with a recursive CTE over a self-join on line_station, but the result is harder to read and test than a dozen lines of Python, and it gains nothing at monthly batch size.
- The departure and cancellation tables (and sql/cancellations.sql) are not needed for the grouping. Only the line and line_station tables matter.

Implementation notes for netmap/groups.py:
- Read line_id from line and (line_id, station_code) from line_station. Include lines with no shared stations as families of one, so every line gets a colour.
- Return a stable mapping, for example each line_id to a family number, numbered in order of the smallest line_id in the family, so the colours do not shuffle between monthly runs.
- Test with a small fixture: a chain A-B-C where A and C share no station, a pair that shares one station, and an isolated line.

Caveat: this decision rests on the schema and the sizes given. It has not been run against the real var/rail.db, which is not in the workspace.

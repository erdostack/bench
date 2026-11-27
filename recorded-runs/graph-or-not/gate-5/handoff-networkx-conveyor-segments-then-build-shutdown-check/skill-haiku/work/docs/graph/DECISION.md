# Graph decision

Decision: recursive-sql

Maintenance asked whether the shutdown check in linewatch needs a graph database, an in-process graph library, recursive SQL or no graph at all. The check is a walk of data-dependent depth (does each station still reach a dock along one-way segments, with bypass segments excluded), and it runs over an edge set of at most 1,500 rows, so recursive SQL on the layout file meets it. The finding it turns on: one recursive query over at most 640 stations and 1,500 segments per check, and about 30 checks a day, is about 45,000 edge reads a day.

## Workload facts

- 640 stations and 1,500 conveyor segments in the layout file (stated by the user)
- Segments run one way; a station is cut off when its parts can no longer reach any dock; bypass segments do not count because they are hand-operated (stated by the user, engineering rule)
- Layout changes a few times a year (stated by the user)
- About 30 shutdown checks a day (stated by the user)
- The layout is a SQLite file kept by line engineering, schema in `db/schema.sql`: two tables, `station` and `segment`, with primary keys only and no other indexes (`db/schema.sql`, `README.md`)
- `var/layout.db` is gitignored and is not in the repository, so the real counts and fan-out were not available (`.gitignore`, directory listing)
- Derived: average out-degree = 1,500 segments / 640 stations = 2.34 (from the two numbers stated by the user)
- Derived: rows one check can read = at most 1,500 segment rows and 640 station rows; 30 checks x 1,500 = 45,000 segment reads per day, upper bound (from the two numbers stated by the user, multiplied out)
- Existing `linewatch/reach.py`: `neighbours()` unions edges in both directions, so it treats one-way segments as two-way and does not exclude bypass segments; `reachable()` is a forward walk from one start, not a dock test; `reachable()` issues one SQL statement per visited station (`linewatch/reach.py`)
- `linewatch/shutdown.py` holds only the TODO (`linewatch/shutdown.py`)
- networkx 3.7 is already a dependency (`requirements.txt`)
- Measured (synthetic, not the real layout): in-memory SQLite 3.53.1 on Python 3.13.18, a random one-way graph of 640 stations, 1,500 segments, 12 docks and 10% bypass segments. A recursive CTE using `UNION` over the station column, with the station being removed excluded, matched a plain Python reverse walk for all 640 possible removals (0 mismatches). Mean about 2.8 ms per check including the Python call overhead (`measured`: an inline script run in memory; nothing written to disk)
- unknown: the real station and dock counts, and how many docks there are
- unknown: the latency budget for one check; none was stated, and the checks look like an interactive maintenance step
- unknown: whether the real layout file has any index beyond its primary keys, and the SQLite version the line runs
- unknown: whether the real layout uses bypass segments heavily; this affects the walk only by removing edges

## Options considered

- graph-database (a dedicated graph store): rejected, because the walk is over at most 1,500 edges, run about 30 times a day, with no stated online latency budget and no measured failure (see the derived figures above). Adopting a server would add a second stateful system to operate and a feed from the layout file that can drift.
- in-process-library (the edges loaded into memory, for example networkx 3.7 already in requirements): rejected for now, because the rung above holds. It would work at this size, but it adds a copy of the layout in each process and a reload step every time the layout changes, which happens a few times a year. Keep it as the fallback if the recursive query cannot be made to run on the real file.
- recursive-sql (recursive queries on the SQLite file already run): chosen, because the walk starts from the docks, has a depth set by the data, runs on a database that line engineering already keeps, and touches at most 640 stations and 1,500 segments per check (see the derived figures). The query below is the shape the team would use; it has been run against synthetic data only, with no indexes added.

  ```sql
  WITH RECURSIVE live(id) AS (
    SELECT id FROM station WHERE kind = 'dock' AND id <> :x
    UNION
    SELECT s.from_station FROM segment s JOIN live l ON s.to_station = l.id
    WHERE s.kind <> 'bypass' AND s.from_station <> :x)
  SELECT id FROM station WHERE id <> :x AND id NOT IN (SELECT id FROM live) ORDER BY id;
  ```

  The rewrite replaces the per-station loop in `reach.py`, follows only the direction the segments run, and excludes bypass segments. Adding an index on `segment (to_station, kind)` is a suggested fix for the real file; it was not applied here.
- no-graph (plain joins, no traversal): rejected, because the answer depends on a walk to a dock of unknown depth along one-way segments; a single join cannot answer it.

## What would change the decision

- The real layout trial fails: on a read-only copy of `var/layout.db`, `EXPLAIN QUERY PLAN` shows a full `SCAN` of `segment` inside the recursive step after the suggested index, or a sample of checks does not match a brute-force walk using the engineering rule; this would move the work to in-process-library.
- The measured per-check time on the real file exceeds the latency budget the maintenance team sets for this check (that budget is theirs to set; none is in the repository). A failure at that point, measured on the real data, would reopen the choice between in-process-library and recursive-sql on the same evidence.
- Checks are needed online on every status event from the PLC gateway, or for many stations at once in a loop, so that the per-check walk runs thousands of times a day rather than about 30; this would move the choice to in-process-library, with a snapshot reloaded when the layout changes.
- The layout grows well beyond 640 stations and 1,500 segments, or the number of distinct stations a correct walk must visit becomes large relative to the database's memory; this would be re-examined against the real counts.
- A graph-database move would be considered only if the in-process and recursive options both fail on the real data and the traversal depth and call rate grow to the profile in the heuristics; nothing in the current evidence points there.

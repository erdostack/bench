# Graph decision

Decision: in-process-library

The question was how to group the 140 lines of the printed network map into colour families, where lines that connect directly or through other lines share a family, and whether that justifies a graph database, an in-memory library, recursive SQL or no graph. This is a whole-graph connected-components job over about 2,300 line-station rows, run once a month, so the data loaded into memory and grouped with a library (or a few lines of union-find) is enough, and a graph database would add a second store for a monthly batch.

## Workload facts

- The question asked of the connections: connected components of lines, where two lines are linked when they share a station, followed transitively (netmap/groups.py docstring and TODO; line_station table in db/schema.sql). It is a whole-graph algorithm, not a walk from one starting point.
- The only link between lines is the line_station table (line_id, station_code), primary key (line_id, station_code) (db/schema.sql). No line-to-line table exists.
- Stated by the user: 140 lines.
- Stated by the user: 1,100 stations.
- Stated by the user: about 2,300 line-station rows.
- Stated by the user: the map is regenerated once a month, so it is a batch job with a window of a month and no latency budget.
- Stated by the user: someone on the data team suggested a graph database as a first use.
- Size: at most 140 nodes (lines), and at most 2,300 line-station rows, so the in-memory edge list is at most 2,300 entries (the user's numbers). Any line-to-line edge count is below 140 x 139 / 2 = 9,730 pairs.
- Fan-out: 2,300 rows / 1,100 stations is about 2.1 line calls per station on average (sum written out from the user's numbers). The tail (the busiest interchange) is unknown.
- Writes and freshness: the data is a monthly export, `var/rail.db`, SQLite, not committed (README.md, .gitignore), so staleness of up to a month is accepted by the schedule.
- What is operated today: SQLite 3.53.1 on this machine for the export; Python with networkx 3.7 is installed here (checked by importing it). README.md does not list dependencies, so whether networkx is a declared dependency of the repo is unknown.
- What was already tried: nothing recorded; the repo has no migrations, decision records or changelog.
- unknown: the real data. var/rail.db is not in the repo, so nothing was measured; the counts above are the user's.
- unknown: whether a station's lines should join when they only share a station by name, or whether interchange stations with separate platforms have separate codes. Looked in db/schema.sql, where station_code is the primary key.

## Options considered

- graph-database (a dedicated graph database, as the data team suggested): rejected, because 2,300 rows once a month is a batch job on a tiny set, and the result is 140 group labels written once; a second store to run and feed buys nothing.
- in-process-library (the rows loaded into memory, grouped with networkx or with plain union-find): chosen, because the whole input is at most 2,300 rows, the job runs once a month, and connected components is a whole-graph algorithm that a library does in one call. Build a graph with line nodes and one edge from each line to each station it calls at (or join lines by shared station), then take its connected components and keep only the line nodes. Return a mapping from line_id to a family number; sort families (for example by smallest line_id) so the colours do not change from run to run.
- recursive-sql (recursive queries on the existing SQLite database): rejected, because a recursive query walks from a start, and grouping all lines needs a component label for every node, which needs a recursive query per line or a more complex label-propagation query; at 140 lines it also works, but this is more code than the library for no gain, and nothing shows the in-memory option fails.
- no-graph (plain joins, no traversal): rejected, because lines that connect "through other lines" need a transitive walk. A single join on line_station finds only direct connections.

## What would change the decision

- The group rule changing to need depth or distance (for example, lines within two changes of each other) would move this to recursive-sql, if the walk stays small, or stay in-process-library.
- The input growing by orders of magnitude (the line-station row count and the memory limit of the job's process are the measures; the data team sets the limit) or the job running online per request would move this to graph-database only after the SQL and library routes are measured failing.
- Dropping the transitive requirement, so that only directly connected lines share a family, would move this to no-graph.

# Graph decision

Decision: recursive-sql

The question was whether the shutdown check (which stations are cut off when one is taken out) needs Neo4j, networkx, recursive SQL on the layout file, or no graph at all. It is a reachability walk (can a station still reach a dock over one-way, non-bypass segments), so it is not `no-graph`, but the whole layout is 1,500 edges and 640 nodes, so one recursive query on the SQLite file already operated does it: about 1.4 ms per check on a synthetic graph of that size, against about 30 checks a day.

## Workload facts

- The question asked of the connections: for a station X, which other stations can reach no dock once X is removed, walking only along segments in their direction and ignoring `kind = 'bypass'` segments (stated by the user, line engineering's rule).
- 640 stations, 1,500 conveyor segments (stated by the user); fan-out about 1,500 / 640 = 2.3 segments per station (derived from the stated counts); no hub data exists in the repo.
- Layout changes a few times a year (stated by the user); about 30 checks a day (stated by the user); no latency budget is stated, so this is an occasional batch-style lookup.
- Segments run one way; bypass segments do not count because they are hand-operated and need a crew not available on nights (stated by the user).
- Schema: `station(id, code, kind in ('station','dock'), hall)` and `segment(id, from_station, to_station, kind in ('belt','roller','bypass'), length_m)`, with no index on either segment column (db/schema.sql).
- Layout lives in SQLite at `var/layout.db`, kept by line engineering (README.md). The file is git-ignored and not in the repo, so no real measurement was possible.
- networkx==3.7 is pinned in requirements.txt, but nothing in linewatch imports it (linewatch/reach.py, linewatch/shutdown.py).
- `linewatch/reach.py` as started does not match the rule: `neighbours` takes both directions (UNION of from and to), does not filter out `bypass`, and `reachable` walks outward from the station, not toward a dock. It also issues one SQL statement per visited node. It cannot be used as is. `linewatch/shutdown.py` holds only the TODO.
- Required work, derived: a correct walk visits each station at most once, so at most 640 stations and 1,500 segments are touched per check. A `UNION` recursive query deduplicates on the node column, so rows produced are bounded by the distinct nodes (engines.md, SQLite notes).
- Measured on synthetic data, not the real layout: SQLite 3.53.1 in memory, 640 stations (12 docks), 1,500 random directed segments (belt, roller, bypass mixed), index on `segment(to_station)`. The reverse-reachability recursive query below took about 1.37 ms on average per check over all 640 stations. `EXPLAIN QUERY PLAN` showed `SEARCH s USING INDEX (to_station=?)` in the recursive step. This shows the order of magnitude only, since the real layout may be shaped differently.
- Query shape (run on the synthetic data): walk backwards from the docks, excluding X:
  `WITH RECURSIVE ok(id) AS (SELECT id FROM station WHERE kind='dock' AND id<>:x UNION SELECT s.from_station FROM segment s JOIN ok ON s.to_station=ok.id WHERE s.kind<>'bypass' AND s.from_station<>:x)`. The cut-off set is the stations in the same walk with no station excluded, minus the stations in the walk with X excluded, minus X itself. The baseline matters: stations already unable to reach a dock today are not caused by this shutdown and should be reported separately or not at all.
- Memory arithmetic for the in-process option: 1,500 edges, far below any process limit even at hundreds of bytes per edge (about 1,500 x 1 KB = 1.5 MB at a deliberately generous figure; bytes per edge not measured).
- unknown: real `var/layout.db` contents (dock count, real fan-out, cycles, how many stations are already cut off), any latency budget for the check, whether the check runs inside a request or as a report, how many linewatch processes run, and whether the SQLite file is opened read-only by linewatch. Looked in README.md, db/schema.sql, requirements.txt, linewatch/, .gitignore.

## Options considered

- graph-database (Neo4j, as the integration lead proposes for "the plant model"): rejected, because the edge set is 1,500 segments (stated by the user), changes a few times a year and is queried about 30 times a day. There is no deep online traversal at scale, so none of the profile that justifies a second stateful system (server, feed from the SQLite file that can drift, new query language) is present.
- in-process-library (networkx 3.7, already pinned): rejected as the first choice, not because it would fail but because recursive-sql holds and is cheaper: no loader, no reload logic and no second copy of the layout to keep fresh. It would also hold (1,500 edges is tiny), and it becomes the pick if the check needs repeated whole-plant analysis or if the SQL version proves awkward to maintain.
- recursive-sql (recursive CTE on the existing SQLite layout file): chosen, because the required work is at most 640 stations and 1,500 segments per check, the synthetic run took about 1.4 ms per check, and the data and the database are already operated. It needs `CREATE INDEX segment_to_idx ON segment(to_station)` (a proposed change to db/schema.sql, not made here), plus a rewrite of `reach.py` so that it walks backwards from the docks, follows direction, skips bypass and uses one statement per check, not one per node.
- no-graph (plain joins, no traversal): rejected, because "cannot get to any dock" is multi-step reachability along a same-kind relation (station to station), not a lookup across a link table.

## What would change the decision

- The real layout (`var/layout.db`) showing a check taking more than a latency budget that maintenance sets (theirs to set) with the index in place, measured with `EXPLAIN QUERY PLAN` and a timer around the call, would move this to in-process-library.
- The layout growing from 1,500 segments to hundreds of thousands, or changing continuously with readers needing near-live answers, with the SQL measured failing at that size, would move this to graph-database.
- Needing whole-plant analysis (for example, ranking every station by how many others its shutdown would cut off, run for all 640 at once) as an algorithm over the whole graph would move this to in-process-library, using networkx.
- A requirement to change the bypass rule per night (for example, counting bypass segments when a crew is available) would not change the option; it would add a flag to the query.

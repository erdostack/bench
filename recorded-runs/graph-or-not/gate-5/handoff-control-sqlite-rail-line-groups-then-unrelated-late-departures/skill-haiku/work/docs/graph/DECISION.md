# Graph decision

Decision: in-process-library

The data team asks whether the printed-map colour families (lines that connect, directly or through other lines, share a family) need a graph database, and the answer is a whole-graph grouping of 140 lines over 2,300 line-station rows, run once a month, which fits in one process with a grouping of about 13 ms measured on a synthetic sample of that size. The finding is the size and shape: the work is connected components over a graph of at most 9,730 line pairs, so an in-memory structure is enough and no store is needed.

## Workload facts

- The question asked of the connections is: which lines are linked through shared stations, at any number of steps, i.e. connected components of the line graph. This is a walk of unknown depth over the whole graph, not a lookup (`netmap/groups.py` TODO, which raises `NotImplementedError`, so no query runs today; the request states the question).
- Lines: 140 (stated by the user; `netmap/groups.py` docstring gives no count).
- Stations: 1,100 (stated by the user).
- Line-station rows: about 2,300 (stated by the user); `db/schema.sql` table `line_station` with primary key (line_id, station_code) confirms the shape, one row per line calling at a station.
- Size of the line graph: edges are pairs of lines sharing a station. Upper bound from the stated counts: C(140, 2) = 140 x 139 / 2 = 9,730 line pairs. The real count is unknown, since the number of lines per station is not in the repo.
- Depth: unbounded in principle (a chain of lines linked through shared stations); the request does not state a depth limit, and none appears in the repo.
- Fan-out: unknown per station; the average lines per station from the stated counts is 2,300 / 1,100 = 2.1 (arithmetic from the stated figures), so the typical station is shared by about 2 lines, with the tail unknown.
- Load: one batch job per month (stated by the user); no latency budget, concurrency or online calls.
- Writes and freshness: the map is regenerated monthly (stated by the user), so a snapshot read at generation time is enough.
- What is operated today: `var/rail.db`, a SQLite export (`README.md`); `netmap/` is data for the printed map. No graph store, and no graph library is named in the repo.
- Measured: a union-find grouping over a synthetic sample of 2,300 rows, 1,100 stations and 140 lines (random assignment, Python 3.13.18 standard library, `tracemalloc` peak 135 KB) took about 13 ms. Synthetic: the real data's shape is not known, so this is a bound on the cost, not a timing of the real map.
- Sum (stated and derived): 140 lines x 139 / 2 = 9,730 possible line pairs at most, each an edge. At a few hundred bytes per edge in a library structure, that is a few megabytes at most (arithmetic; the bytes per edge are not measured here).
- What was already tried, and what happened each time: unknown. No decision record, changelog or prior grouping code exists in the repo.
- unknown: the real line-station data was not in the repo (`var/` is gitignored and `rail.db` was not present), so the real number of shared stations, the number of colour families and the largest family were not measured. Looked at: `README.md`, `.gitignore`, `db/schema.sql`, `netmap/__init__.py`, `netmap/groups.py`, `sql/cancellations.sql` (a cancellations report, not related to grouping).
- unknown: whether "connect" means sharing a station only, or also sharing a track segment or a timetable interchange; the request and the schema describe station calls only.

## Options considered

- graph-database (a dedicated graph store, as the data team suggested; no product named): rejected, because the whole profile is absent: the graph is at most 9,730 pairs, a monthly batch needs no online traversal or latency budget, nothing is measured failing, and a second stateful system with its own load step would cost more than the job.
- in-process-library (the edges loaded into memory): chosen, because this is a whole-graph result over a snapshot read once a month, the edge set fits trivially in one process (measured 135 KB peak for the 2,300-row sample; arithmetic bound in the Workload facts), and a single grouping ran in about 13 ms. A plain union-find over a dictionary is enough; a graph library is optional.
- recursive-sql (recursive queries on the database already run): rejected for this job, because a recursive query walks from a starting point, while this job needs every family at once with no start line; a recursive query per line would repeat the same walk 140 times and is not shown to meet any need. It is not disproved either, and it would be the next choice only if a per-request walk from one line appeared.
- no-graph (plain joins, no traversal): rejected, because the grouping follows a relation through other lines at unknown depth (a chain of shared stations); a single join or a fixed number of joins does not give the family.

## What would change the decision

- A requirement for an online, per-request traversal from a single line (for example, "all lines reachable from this line" in a timetable tool) would move this to recursive-sql while the data stays in `var/rail.db`, and to graph-database only if that walk ran deep and online over an edge set too large for a copy per process, which 9,730 pairs does not approach.
- The real line-station data showing a much larger line graph than the bound (the bound is the stated counts; a count of distinct shared-station pairs above a few hundred thousand would change the memory arithmetic) would need its own measurement before choosing a structure. The owner of the map sets that limit; the repo sets none.
- A stated freshness requirement shorter than the monthly regeneration (for example, live map updates) would move this to a service that holds the structure and applies changes, which is a datastore decision and not the data team's suggestion as stated.

Nothing in the repo was changed.

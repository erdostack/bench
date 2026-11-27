# Graph decision

Decision: recursive-sql

The question is whether the monthly headcount rollup, each unit's people plus everyone in the units below it, needs a graph database, an in-memory graph library, recursive SQL, or no graph at all. The walk goes up or down a tree at most 8 levels deep over about 1,900 units and 23,000 people, which the SQLite unitbook already holds with indexes on the parent column, so the rollup stays in SQL; the finding that turns it is the depth bound, which keeps the walk to a few hundred thousand rows per run.

## Workload facts

- Units: about 1,900 (stated by the user); unit table in db/schema.sql with unit_parent index on parent_id.
- Depth: at most 8 levels from the top of the organisation to the smallest team (stated by the user). A walk down from any unit is at most 7 hops; a walk up from any person's unit is at most 8 levels (derived from the stated depth).
- People: 23,000 (stated by the user). Assignment rows: count unknown; person table has 23,000 rows per the stated figure, assignment rows are not stated.
- Walk: parent-to-child on unit (a relation between things of the same kind), a walk to a bounded depth, so the rung is a walk from a starting point (heuristics.md, "A walk from a starting point").
- Upper bound on the work, from the stated numbers: each assignment walks up at most 9 rows (its own unit plus 8 ancestors), so a rollup produces at most 9 x A (person, unit) pairs, where A is the assignment count. With A equal to 23,000 (one current assignment each, unknown), that is at most 207,000 rows. With A unknown, the bound is 9 times A.
- Indexes present: unit primary key (for the upward step), unit_parent on unit(parent_id) (for the downward step), assignment_unit on assignment(unit_id, start_date) (for the join to people by unit and date) (db/schema.sql).
- Frequency: monthly run plus the odd ad-hoc rerun (stated by the user). Batch, not online; no latency budget stated.
- Freshness: unitbook refreshed nightly from the HR system (README.md).
- What is operated today: one SQLite file, var/unitbook.db (README.md), Python 3.11+ standard library only (README.md); SQLite version unknown.
- Existing report: reports/assignments_by_unit.sql counts direct assignments only, so the rollup is new work; the runner executes a SQL file with named parameters (orgunits/run.py).
- Measured: none. var/unitbook.db is absent from the working copy (var/ is gitignored), so no row count, plan or timing could be taken.
- unknown: assignment row count A; whether closed units (unit.closed_on set) count toward a parent's headcount; whether a person can hold two overlapping assignments (which would double count if rows are counted rather than distinct people); SQLite version; the timing on the real file.

## Options considered

- graph-database (a dedicated graph store): rejected, because a monthly batch over at most 8 levels and about 1,900 units needs no separate store, and nothing measured shows SQLite failing; adopting a server would add a second copy of the tree, a load step and a query language for one report.
- in-process-library (networkx or a dictionary of child lists loaded into the reporting job): rejected for now, because it would also fit (1,900 units is small), but recursive-sql is the cheaper rung and holds on the arithmetic above, so it comes first. Reconsider only if the rollup has to run online with many concurrent requests.
- recursive-sql (recursive queries on the SQLite database already run): chosen, because the walk is bounded at 8 levels, both steps are indexed (unit primary key and unit_parent), and the rows it produces are at most 9 x A (about 207,000 at 23,000 assignments), which is small for a monthly batch. Not timed on the real file; the bound is arithmetic from the stated numbers.
- no-graph (plain joins, no traversal): rejected, because the rollup walks the tree to a depth of up to 8 levels; a single join cannot reach units several levels below.

## What would change the decision

- The rollup has to answer online, per request, for many users at once with a latency budget, and the recursive query is measured over the latency limit on the real file (sample EXPLAIN QUERY PLAN and timing on SQLite). Then reconsider in-process-library, since the tree fits in memory.
- The tree grows far past 8 levels or past the stated 1,900 units, so the bounded walk no longer has a bound. The owner of the org chart (HR) sets the limit.
- Whether closed units count, and whether assignments overlap, must be answered before the rollup is written; neither moves the decision between options, but both change the numbers.
- Measured on the real var/unitbook.db: a recursive query with the unit_parent index showing SCAN rather than SEARCH on the parent column in EXPLAIN QUERY PLAN means the index is not used, which is a fix to the query, not a reason to leave SQL.

Nothing in the repo was changed beyond this file.

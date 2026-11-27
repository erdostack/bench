# Graph decision

Decision: recursive-sql

HR wants each unit's headcount to include everyone in the units below it (unit.parent_id), and an analytics colleague (Ines) suggested moving the unit tree into a graph database. Keep it in the unitbook SQLite file and do the rollup with one recursive query: the tree has about 1,900 units, at most 8 levels, and the pack runs once a month, so the whole rollup touches at most 1,900 units times 8 ancestor levels, about 15,200 rows, before it reaches the 23,000 people.

## Workload facts

- Units: about 1,900 (stated by the user).
- Depth: at most 8 levels from the top to the smallest team (stated by the user). db/schema.sql gives each unit one nullable parent_id (NULL for the top), so it is a tree: one route from any unit to the top, no multiple paths.
- People: 23,000 (stated by the user).
- Load: the pack runs once a month plus the odd ad-hoc rerun (stated by the user). A batch job over a small snapshot, no online latency budget.
- Storage: all in the unitbook SQLite file `var/unitbook.db`, refreshed nightly from the HR system (stated by the user; README.md). The file is not in the repo.
- The question asked of the connections: for each unit, count the people assigned to it or to any unit below it. A walk of data-dependent depth along parent_id, aggregated; today reports/assignments_by_unit.sql counts direct assignments only (no recursion) for :as_of, using the condition start_date <= :as_of AND (end_date IS NULL OR end_date >= :as_of).
- Indexes: unit_parent on unit(parent_id) and assignment_unit on assignment(unit_id, start_date) already exist (db/schema.sql), so a walk down parent_id and the join to assignment are both indexed.
- Upper bound on the walk: each unit appears under at most 8 ancestors including itself, so a unit-to-ancestor table has at most 1,900 x 8 = 15,200 rows (derived from the stated figures); this is exact work, not waste, and it is small.
- Tooling: Python 3.11+, standard library only (README.md); orgunits/run.py runs one .sql file with named parameters through sqlite3. A recursive query fits this runner as one more file in reports/.
- unknown: number of rows in assignment (history over time, not only current), since only the people count was given. The `as_of` filter bounds it to current rows, but the table size is not in the repo.
- unknown: whether closed units (unit.closed_on) should be included for the as_of date, and whether a person assigned to more than one unit on the same date counts once per unit or once overall at a rollup. These are reporting rules for HR to state, not workload facts; the query needs a stated rule (see the last section).
- Nothing was run: the database is not in the repo, so no row counts, plans or timings were taken.

## Options considered

- graph-database (a dedicated graph store, as Ines suggests): rejected, because the data is 1,900 units and 8 levels in a monthly batch with no latency budget; a second stateful system and a nightly feed from the HR system would add cost for a rollup that touches about 15,200 unit-ancestor pairs.
- in-process-library (the edges loaded into memory): rejected, because it is not needed; the data already sits in SQLite and recursive SQL does the same job in one statement, without loading and keeping a second copy in Python. It would fit easily in memory, so this is not a capacity reason.
- recursive-sql (a recursive CTE on the SQLite database already used): chosen, because the walk goes from each unit down a tree of at most 8 levels over 1,900 rows, parent_id and assignment(unit_id, start_date) are indexed, and the pack runs monthly. Suggested shape (not applied; nothing in the repo besides this file was changed): a WITH RECURSIVE that builds (ancestor_id, unit_id) pairs starting from (id, id) and following unit_parent downwards, join to the current assignments for :as_of as in reports/assignments_by_unit.sql, and `COUNT(DISTINCT a.person_id)` grouped by ancestor_id, so a person with two current assignments below the same unit is counted once. Add it as a new file in reports/ and keep the direct-only report as it is.
- no-graph (plain joins, no traversal): rejected, because a rollup that includes everyone in the units below follows parent_id for a depth that depends on the data (up to 8 levels); one join per level would fix the depth in the query, and the walk is cleaner as a recursion.

## What would change the decision

- A rollup run measured on the real var/unitbook.db taking longer than the pack can wait (HR to set the limit; for a monthly pack, minutes is the order of magnitude to ask about): this would move it to in-process-library, since 1,900 units would load in well under a second, and the aggregation could be done in Python.
- The unit tree growing by orders of magnitude (for example to millions of units), or depth beyond the stated 8 levels with many parents per unit: re-check the arithmetic; a unit having more than one parent would also break the tree assumption and the count-once rule.
- HR requiring interactive, many-times-a-day rollups with a latency budget over the full history: ask for the call rate; this alone would not point to a graph database unless SQL is measured failing at that rate.
- A rule from HR that closed units or concurrent assignments are treated differently: this changes the query's filters, not the option.

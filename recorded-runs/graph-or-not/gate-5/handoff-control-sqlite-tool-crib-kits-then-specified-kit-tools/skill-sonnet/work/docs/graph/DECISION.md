# Graph decision

Decision: recursive-sql

The "what's in this kit" page needs every tool in a kit, including tools in kits packed inside it, walked from one starting kit down at most 4 levels. That is a descendants walk, and a recursive query on the existing SQLite file covers it: the whole crib is about 3,610 items, so even a walk that touched every item is a few thousand rows, at about 50 views a day.

## Workload facts

- 3,200 tools and 410 kits in the crib's SQLite file (stated by the user)
- Kits nest up to 4 deep (stated by the user)
- The page gets about 50 views a day, from the crib attendants (stated by the user)
- The automation engineer wants to put the crib in a graph database (stated by the user)
- Question asked: all tools in one kit, including kits packed inside it, as a walk down `kit_line` (kit_id -> item_id, where item_id may itself be a kit) from a single starting kit; no whole-graph algorithm (crib/kits.py TODO, db/schema.sql)
- Only the first level is implemented today, one statement filtered by `kit_id` (sql/kit_first_level.sql, crib/kits.py)
- Edge table is `kit_line` with primary key (kit_id, item_id), so the column a downward walk enters by is already indexed (db/schema.sql)
- Items in total: 3,200 + 410 = 3,610, which caps the distinct nodes any one walk can visit (stated by the user, summed here)
- Load: 50 views/day is about 50 / 86,400 = 0.0006 views per second, so effectively no concurrency (stated by the user, derived here)
- Operated today: one SQLite file `var/crib.db`, Python 3.12, Flask, queries as `:named` files in `sql/` (README.md)
- unknown: edge count in `kit_line` and fan-out per kit; no database file is in the repo (`var/` is git-ignored), so nothing was measured
- unknown: write rate and how stale a page may be; nothing in the repo states either
- unknown: whether the packing data can contain a cycle (a kit packed inside itself); the schema has no constraint against it
- unknown: SQLite version in production; the repo pins none
- Nothing was run and nothing in the repo besides this file was changed.

## Options considered

- graph-database (a dedicated graph database, as the automation engineer proposes): rejected, because the walk is at most 4 levels over at most 3,610 items at about 50 views a day, with no measured failure of SQL to point to; the second stateful system and feed from SQLite buy nothing here.
- in-process-library (load the data into memory and use a graph library): rejected, because it adds a load and reload step and a second copy of data that already sits in the one SQLite file, when a single query from a starting kit does the job.
- recursive-sql (recursive queries on the SQLite file already run): chosen, because the question is a descendants walk from one kit, the entry column is already indexed by the primary key, and the required set is bounded by 3,610 distinct items. Write it as one recursive CTE in a new file under `sql/`, use `UNION` (not `UNION ALL`) on item ids only, with no path or depth column, so an item reachable by several routes is visited once and a cycle cannot loop, then join to `crib_item` and keep `kind = 'tool'`. Do not issue one statement per level from Python. If quantities are shown, sum `qty` along each route separately, since a tool packed in two kits has two quantities.
- no-graph (plain joins, no traversal): rejected, because a kit packed inside a kit is a relation between items of the same kind followed for more than one step, up to 4 levels.

## What would change the decision

- The recursive query measured on the real `var/crib.db` taking longer than the attendants will wait on a page (a latency limit the crib owner sets), after the single-statement, `UNION` form is in place, would move this to in-process-library or graph-database depending on the data size then.
- The crib growing so that one walk visits tens of thousands of distinct items, or views rising from about 50 a day to many at once, would reopen this; today's figures are 3,610 items and 0.0006 views per second.
- A requirement for whole-graph analysis (for example which tools are in the most kits across the crib) run as a batch job would move this to in-process-library.
- Nesting deeper than 4 levels by itself would not change it; depth is not the limit here, the number of distinct items is.

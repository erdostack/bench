# Graph decision

Decision: recursive-sql

The question: gross requirements of every bought-in part for N mowers, all the way down the BOM, with 4% scrap compounding at each level, and a consultant's suggestion of a graph database. The answer is recursive SQL on the Postgres already operated: the walk is a descendants-with-quantities explosion, and the biggest ride-on BOM came back in 0.4 s against a 3 s budget.

## Workload facts

- The question asked of the connections: for one item and quantity, every descendant through bom_line (parent_id to component_id, qty_per), depth depends on the data, with a product of qty_per and the scrap factor along each path and a sum per bought part (db/schema.sql; the TODO in planning/orders.py; sql/bom_first_level.sql shows only the one-level query that runs today).
- 48,000 items and 210,000 BOM lines in Postgres 16 (stated by the user; README.md names Postgres 16 as production).
- Average fan-out: 210,000 / 48,000 = 4.4 components per item (derived from stated numbers); maximum depth 11 levels, from the deepest BOM (stated by the user).
- Load: maybe 300 of these a day, an online screen with a budget of under 3 seconds (stated by the user): 300 / 86,400 s = 0.0035 calls per second, so almost never concurrent.
- Measured by the user: a recursive query on a copy for the biggest ride-on mower came back in 0.4 s (stated by the user). This is the worst-case product, so the typical order is cheaper. The plan and the exact query were not provided; the scrap compounding is not shown to have been part of that run (unknown).
- Rule from the planning lead, firm (stated by the user): add 4% scrap on every BOM line, compounding down the levels, so a part three levels down gets it three times (a factor of 1.04^3). It is a need, not a claim about the data.
- Indexes: PRIMARY KEY (parent_id, component_id) serves the walk down from a parent; bom_line_component (component_id) serves where-used and is not needed here (db/schema.sql).
- Items and BOM lines are copied nightly from PLM, so data is static during the day (README.md).
- Queries live as plain files in sql/ with :named parameters, run by planning/sqlfile.py, and each has to work on both Postgres and SQLite, the test database (README.md, planning/sqlfile.py). WITH RECURSIVE works on both.
- Checked: on a four-item SQLite test (A made of 2 x B and 1 x C, B holds 3 x P, C holds 5 x P, order of 10), the query below returned 118.976 for P, equal to 10 x (2 x 3 x 1.04^2 + 1 x 5 x 1.04^2) (measured, SQLite 3.53.1, Python 3.13).
- unknown: the number of distinct components under the biggest mower and the number of routes (rows) the walk returns, because there is no query plan or row count in the request or repo; the 0.4 s is the stated measurement standing in for that. unknown: whether BOMs can contain cycles; the schema does not forbid them.

## Options considered

- graph-database (a dedicated graph store, as the consultant suggests): rejected, because the walk already measures 0.4 s against a 3 s budget in Postgres at the full size, at about 0.0035 calls a second; a second store would add a nightly feed from PLM and a new query language with nothing to fix.
- in-process-library (the BOM edges loaded into memory): rejected, because 210,000 lines would be copied into every process and rebuilt after each nightly load, to speed up something that already meets the budget.
- recursive-sql (recursive queries on the Postgres already run): chosen, because the question is a walk from one item at data-dependent depth, the primary key already provides the index the walk enters by, and the measured 0.4 s is over seven times inside the budget (3 / 0.4 = 7.5). Shape of the fix (not applied here): put it in sql/ as one WITH RECURSIVE query that starts at :item_id with need = :qty, joins bom_line on parent_id, and multiplies need by qty_per x 1.04 at every step; then sum need grouped by part for items with make_buy = 'B'. The compounding comes from multiplying 1.04 once per level, not from the quantity. It returns a row per route, and a part reachable many ways is correctly counted once per route for a sum.
- no-graph (plain joins, no traversal): rejected, because the depth runs to 11 levels and depends on the data, which a fixed set of joins cannot follow.

## What would change the decision

- The same recursive query, with the 4% compounding included, measured above 3 s at the 95th percentile on a real full-size copy would move this to in-process-library, if the nightly-loaded 210,000 lines fit in the memory of each process, because then SQL has been measured failing; no such measurement exists.
- A BOM containing a cycle would make the plain recursive query loop; that is a data fix or a depth guard of 12 levels, not a reason for another engine.
- Calls rising from 300 a day to many a second, or the BOM changing continuously instead of nightly, with SQL measured failing at that load, would be the conditions for reconsidering graph-database. Nothing in the request points there.

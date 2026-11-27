# Graph decision

Decision: recursive-sql

The question: a rolled-up unit cost for the quoted item (made = labour_cost + qty x rolled cost of each component, bought = std_cost), with no cost at all if anything under the assembly is missing from the item table, and Piotr's proposal to move the BOMs to a graph database. The answer is recursive SQL on the existing SQLite file: it is a walk down from one item to a data-dependent depth, over 31,000 lines, about 200 times a day. A synthetic run at that size answered in at most 0.13 s per quote.

## Workload facts

- Question asked: one item's descendants through bom_line (parent_id to component_id, both pointing at item), depth depends on the data, rolled up with a product of qty along each path and a sum at the end; the TODO is in quotecalc/quote.py, no query exists yet (quotecalc/quote.py, db/schema.sql).
- 9,000 items, 31,000 BOM lines (stated by the user).
- BOMs up to 7 levels (stated by the user).
- About 200 quotes a day (stated by the user), an online page but about one call every few minutes on average: 200 / 86,400 s = 0.0023 calls per second, so almost never two at once.
- All data is in the SQLite file loaded from the ERP export (stated by the user); var/quotes.db is rebuilt from CSV by quotecalc/load.py, so writes are a full reload, not a continuous stream (quotecalc/load.py).
- About 300 BOM lines point at items no longer in the item table since the spring ERP purge; schema declares REFERENCES but SQLite does not enforce it without PRAGMA foreign_keys, and the loader does not set it (stated by the user; db/schema.sql, quotecalc/load.py). The sample export shows the same thing: bom_line 3,41 has no item 41 (data/bom_lines.csv, data/items.csv).
- Finance rule, firm (stated by the user): if anything anywhere under an assembly is missing from the item table, the assembly gets no cost at all; the quote page shows it as incomplete, never a partial total.
- Piotr wants a graph database "so the references are real" (stated by the user). A graph store does not make the purged items reappear; the 300 dangling lines have to be detected either way.
- bom_line has PRIMARY KEY (parent_id, component_id), so SQLite already has an index that a walk entering by parent_id uses; the plan shows SEARCH b USING INDEX sqlite_autoindex_bom_line_1 (parent_id=?) at the recursive step (measured, EXPLAIN QUERY PLAN on SQLite 3.53.1).
- Measured on a synthetic in-memory database built with the repo's db/schema.sql: 9,000 items, 31,000 lines, 8 item levels (7 levels of BOM lines), 150 purged components. One recursive query with one row per route, LEFT JOIN to item to flag missing, run for 200 top-level items: total 4.8 s, worst single call 0.125 s, mean 9,821 rows and maximum 34,440 rows per call. This is random data, not the real export, so it only shows the order of magnitude (measured, Python 3.13 sqlite3, SQLite 3.53.1).
- 200 quotes a day x worst case 0.125 s = 25 s of query time a day (derived from the two figures above).
- unknown: the real fan-out, how many parts are shared between assemblies, and the real worst-case route count for the biggest assembly; only a 7-row sample export is in the repo (data/*.csv). unknown: the quote page's latency budget; none is stated in the repo or the request.
- unknown: memory limit of the process and number of processes serving the quote page; not needed for this decision, since nothing is loaded into memory.

## Options considered

- graph-database (Piotr's proposal, a dedicated graph database): rejected, because the walk is 7 levels over 31,000 lines at about 200 calls a day, which SQLite measured at 0.125 s worst case on synthetic data of that size, and because it would add a second store plus a nightly feed while leaving the 300 dangling lines exactly as they are.
- in-process-library (the edges loaded into memory): rejected, because it adds a loader and a copy of the data to keep fresh for no gain over a query that already answers in about a tenth of a second; it would also be reasonable if the recursive query were measured too slow on the real export, which has not been shown.
- recursive-sql (recursive queries on the SQLite file already run): chosen, because the question is a walk from one item at data-dependent depth, the edge index already exists via the primary key, and the measured cost is small against about 200 calls a day. Shape of the fix (not applied here): one recursive CTE from the quoted item carrying a running multiplier mult = product of qty, LEFT JOIN item at each step, and a missing flag; the unit cost is NULL if any reached component has no item row, otherwise the sum of mult x std_cost over bought rows plus mult x labour_cost over made rows. Return None for unit_cost and an "incomplete" marker in that case so the page never shows a partial total. The query returns a row per route, so a part reachable by many routes is counted once per route, which is correct for the quantity sum; if the real data shows route counts in the hundreds of thousands, roll up level by level with GROUP BY instead.
- no-graph (plain joins, no traversal): rejected, because the cost of a made item depends on components of components down to 7 levels, which one join across bom_line cannot express.

## What would change the decision

- A recursive query on the real quotes.db with the worst-case assembly taking more than the quote page's budget (whoever owns the page sets it; none is stated) would move this to in-process-library, if the whole edge set fits in memory (31,000 lines is small), or to a level-by-level rollup before anything else.
- Quote volume growing from about 200 a day to a rate where several walks run at once all day, together with measured failures, would be worth re-measuring, but would still point at in-process-library before graph-database.
- BOM data growing orders of magnitude beyond 31,000 lines, changing continuously and being read online with SQL measured failing at the needed depth, would move this to graph-database. Nothing in the evidence points there now.
- Finance changing the incomplete rule (for example allowing partial totals) would not change the engine, only the query's missing-flag handling.
- Fixing the 300 dangling lines at source (restoring items, deleting lines, or enabling foreign keys in the loader) is a data-quality decision for the ERP owners; it is not a reason to change engine.

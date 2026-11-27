Decision: recursive-sql

Use a recursive query on the SQLite file you already run; no graph database or graph library is needed.

What it turns on:
- The page is a descendants walk from one kit, at most 4 levels deep. That is a relation between items of the same kind followed more than once, so it is not "no-graph", but it is a walk SQL handles.
- The most any walk can touch is 3,200 + 410 = 3,610 distinct items, and the page gets about 50 views a day (about 0.0006 per second). A graph database would be a second stateful system, with a feed from SQLite, for a few thousand rows.
- `kit_line` has primary key (kit_id, item_id), so the column the walk enters by is already indexed.

How to write it: one recursive CTE in a new file under `sql/`, called from `kit_page` in `crib/kits.py`, not one statement per level from Python. Use `UNION` (not `UNION ALL`) on item ids only, with no path or depth column. An item reachable by several routes is then visited once, and a cycle cannot loop. Join to `crib_item` and keep `kind = 'tool'`. If you show quantities, multiply `qty` along each route, since a tool packed in two kits has two quantities.

What I could not find or measure:
- No database file is in the repo (`var/` is git-ignored), so I ran nothing. The edge count, fan-out per kit and query timing are unknown.
- Write rate and how stale the page may be are not stated anywhere.
- The schema does not prevent a kit being packed inside itself, so it is unknown whether cycles exist in the data.

What would change this: the query measured on the real `var/crib.db` being too slow for the page, a latency limit that you set; the crib growing to tens of thousands of distinct items per walk or many simultaneous views; or a batch whole-crib analysis (that would point to an in-process library).

I wrote `docs/graph/DECISION.md` with the facts, options and these conditions. Nothing else in the repo was changed.

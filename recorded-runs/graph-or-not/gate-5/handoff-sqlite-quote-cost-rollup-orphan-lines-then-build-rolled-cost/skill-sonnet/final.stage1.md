Decision: recursive-sql

Keep this on SQLite. The roll-up is a walk down one item's BOM to a depth that depends on the data (up to 7 levels), over 31,000 lines, about 200 times a day. That is a small job for a recursive query, and a graph database would not fix the actual mess.

The numbers it turns on:
- bom_line's primary key (parent_id, component_id) already gives the walk an index. EXPLAIN QUERY PLAN shows the recursive step searching by parent_id, not scanning.
- I ran the query on a synthetic in-memory database built with your schema: 9,000 items, 31,000 lines, 7 BOM levels, 150 components purged. The worst single call took 0.125 s and the largest call returned 34,440 rows. 200 quotes a day at that worst case is about 25 s of query time a day. It is synthetic data, not your export, so treat it as order of magnitude.
- The 300 dangling lines are a data problem, not a storage problem. A graph database would not bring the purged items back, and you would still need to detect the missing ones. The sample export shows it too: line 3,41 points at an item 41 that is not in the item table.

How to build it (I did not change any code): one recursive CTE from the quoted item, carrying a running multiplier (product of qty down the path) and LEFT JOINing item at each step to flag components with no item row. If any reached component is missing, return unit_cost None and mark the quote incomplete. Otherwise unit cost is the sum of multiplier x std_cost for bought rows plus multiplier x labour_cost for made rows, which gives Finance their no-partial-totals rule. This returns one row per route, which is right for summing quantities. If the real worst-case assembly produces hundreds of thousands of routes, switch to a level-by-level roll-up with GROUP BY.

Not found or not measured: the real fan-out and sharing of parts (the repo has only a 7-row sample export), the real worst-case assembly, and the quote page's latency budget. Please run the query on the real quotes.db for your biggest assembly before shipping. A graph database or in-memory library only becomes worth discussing if that run is too slow for the page, or the BOM grows by orders of magnitude.

I wrote docs/graph/DECISION.md and changed nothing else in the repo.

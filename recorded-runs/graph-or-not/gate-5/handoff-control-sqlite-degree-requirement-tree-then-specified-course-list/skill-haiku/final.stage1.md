Decision: recursive-sql

Keep the audit in the SQLite database and write the sub-requirement walk as a recursive query over the parent index. The requirement tree is at most 5 levels deep, the catalogue is 1,900 requirements and 14,000 listings, and the page gets about 2,000 views a day. A dedicated graph database would add a second copy rebuilt each term and a server to run, for a page with very little load outside registration week.

Numbers it turns on: at most 5 levels; 14,000 listings. Each view touches at most the whole catalogue, 1,900 requirements and 14,000 listing rows, and 2,000 views a day is about 0.023 views per second on average. These are upper bounds from your numbers, not timings.

Not found or not measured: the real var/audit.db is absent from the working copy, so I took no plan or timing. The page's latency budget and the peak view rate are unknown. Two things to get right when the walk is written: count each course once, since a course can sit under several sub-requirements, and avoid a UNION ALL walk, which returns one row per route.

Nothing in the repo was changed beyond the new file docs/graph/DECISION.md under /run/work.

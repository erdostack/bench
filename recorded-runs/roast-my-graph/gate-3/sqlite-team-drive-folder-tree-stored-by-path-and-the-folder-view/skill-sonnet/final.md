The folder view is over budget because of one statement: `queries/subtree.sql`. It uses `path LIKE :prefix || '%'`. SQLite only turns LIKE into an index range for a literal or a bound parameter, not a concatenation. The plan on drive.db is `SCAN node USING INDEX sqlite_autoindex_node_1`, so every call reads the whole path index. On the 120k sample a 7-row folder takes about 47 ms. Production has about 3 million nodes, so I estimate 0.8 to 1.2 s per call by scaling that up. I did not measure that.

What to change:
1. Replace the LIKE with a range on the unique `path` index you already have:
   ```sql
   WHERE path > :prefix
     AND path < substr(:prefix, 1, length(:prefix) - 1) || '0'
   ORDER BY path
   ```
   I ran this on drive.db. The plan becomes `SEARCH ... (path>? AND path<?)` and the results are identical to the LIKE version for four folders. The 7-row folder drops from 47 ms to 0.1 ms, and `/web-8/` (4,375 rows) from 53 ms to 22 ms. No new index is needed.
2. The biggest folders still cost too much, because of how many rows they return. On the sample, 39,865 rows take about 138 ms and 106,766 rows about 340 ms. `folder_view` returns every descendant, so indexing alone will not get those under 100 ms. Page the result with `LIMIT` and `path > :after`, or state the budget per page. This is a question for whoever owns the UI, since the README says the view shows everything.
3. Two low items, both safe as written:
   - Nothing in these files rewrites `path` when a folder is renamed or moved. All 120,000 sample rows agree today.
   - `queries/breadcrumbs.sql` has no depth guard. There are no loops in the data, and the maximum depth is 53.

`queries/children.sql` and `node_parent` are fine: the biggest folder has 48 children and the query takes under 1 ms.

Files are in the repo root, and the full roast is at docs/graph/ROAST.md:
- findings.json
- docs/graph/ROAST.md

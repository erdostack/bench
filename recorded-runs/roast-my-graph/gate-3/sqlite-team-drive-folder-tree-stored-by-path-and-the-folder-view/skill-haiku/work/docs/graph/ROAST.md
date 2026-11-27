# Roast: drive folder view (schema.sql, queries/, drive/)

Verdict: Not nothing serious. The folder view can't hold 100 ms for big folders for two reasons: `queries/subtree.sql` filters with a LIKE that makes SQLite scan the whole `node.path` index, and it returns every descendant with no limit. The first is a fix with no product cost. The second needs a decision about paging or summaries. `children.sql` and `breadcrumbs.sql` are sound at this size.

Judged against:
- Engine: SQLite 3.53.1, read-only sample (drive.db), from the engines notes in this skill.
- Node count: about 3 million in production, 120,000 in the sample (README.md).
- Budget: the folder view must answer in under 100 ms and show everything under a folder at any depth (README.md, queries/subtree.sql).
- Sidebar: `queries/children.sql` lists one level (README.md).
- Header: `queries/breadcrumbs.sql` walks up for the header (README.md).
- Schema: `node` with `path TEXT NOT NULL UNIQUE` and `node_parent ON node(parent_id, name)` (schema.sql).
- Names: lower-case letters, digits, `-` and `.`, so paths never contain `%` or `_` (README.md, schema.sql).

## Findings

### high: `queries/subtree.sql`
Problem: `WHERE path LIKE :prefix || '%'` gives `SCAN node USING INDEX sqlite_autoindex_node_1` in EXPLAIN QUERY PLAN on drive.db, so the UNIQUE index on `node.path` is read in full on every folder view. The sample has 120,000 nodes and the README says production has about 3 million, so each request reads about 25 times more rows (an estimate from the row counts).
Fix: Use a range on the same index: `WHERE path >= :prefix AND path < :upper AND path <> :prefix ORDER BY path`, where `:upper` is the prefix with its final `/` replaced by `0`. The plan becomes `SEARCH node USING INDEX sqlite_autoindex_node_1 (path>? AND path<?)`. Measured on drive.db: 4,375 rows went from 21 ms to 9 ms; 58,545 rows from 141 ms to 127 ms; 106,766 rows from 276 ms to 241 ms.

### high: `queries/subtree.sql`
Problem: No `LIMIT` and no keyset paging, so the view returns every descendant. `/shared-4/` returns 106,766 rows and took 241 to 276 ms on this machine, which is already over the README's 100 ms budget. At production size a top-level folder can return millions of rows in one request, and no index brings that under 100 ms.
Fix: Page on the key: `WHERE path > :after AND path < :upper ORDER BY path LIMIT :page_size`, passing the cursor back from the client. Or show children with a folder size stored and maintained on write. The product has to choose: the README asks for everything under a folder at any depth and for under 100 ms, and both cannot hold at production size.

### medium: `drive/tree.py`
Problem: `folder_view` passes `folder_path` into the LIKE without escaping `%` or `_`. `/shared_4/` returns 106,767 rows from `/shared-4/`, because `_` matches any character. Nothing validates `folder_path`. The defect needs a caller that sends such a path, so it is rated medium.
Fix: Compare the prefix as a literal, as in the range fix above. Also validate `folder_path` against the same character set as the `node.name` CHECK in schema.sql before the query runs.

### low: `path`
Problem: `node.path` stores the full ancestor chain as text beside `parent_id`. The sample agrees with itself (0 mismatches between `path` and parent `path` plus name), but nothing in the repo writes node rows, so nothing shown keeps them in step. A folder move would have to rewrite every descendant's path. Question to confirm.
Fix: Confirm that moves and renames rewrite every descendant `path` in one transaction, and keep the parent-consistency check in the tests.

## Holds up
- `node_parent` (`parent_id, name`): serves `children.sql` as a `SEARCH` on `parent_id`. The `ORDER BY kind DESC, name` uses a temp B-tree over one folder's children, and the largest folder in the sample has 48 children, so the sort is cheap here. It would change if a flat folder grew into the thousands.
- `breadcrumbs.sql`: the recursion walks one primary-key search per level and stops at the root, so its depth is the folder depth. Every sample node's `path` equals its parent's path plus name, and a `path` that strictly lengthens on each step rules out a loop along the chain. A loop would need a write that breaks that rule, and no writer is in the repo.
- The recursive-CTE alternative for `subtree.sql` (walking `parent_id` with `node_parent`) returned the same rows but was slower: 496 ms against 276 ms for the 106,766-row folder. It is not the fix, and the range form is.

## Not checked
- Production size was not measured. The 25 times figure is the row-count ratio, and the timings are for this sandbox, not for the production server.
- EXPLAIN QUERY PLAN and timings were run read-only on drive.db with SQLite 3.53.1. The `:upper` bound (prefix with `/` replaced by `0`) relies on `/` being the character just below `0` in byte order, which holds for ASCII and the sample's paths.
- No writer for `node` rows is in the repo, so the `path` copy and the `parent_id` foreign key are not checked for upkeep. The foreign key is not enforced unless the application turns on `PRAGMA foreign_keys`.
- The permission model for folder views is not in the repo.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

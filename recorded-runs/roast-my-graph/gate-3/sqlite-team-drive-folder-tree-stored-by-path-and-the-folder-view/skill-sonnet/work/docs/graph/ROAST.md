# Roast: drive folder view (schema.sql, queries/, drive/tree.py, drive.db sample)

Verdict: The folder view is slow because `queries/subtree.sql` cannot use the index it already has, so every folder view reads the whole `path` index, whatever the folder's size. Fix that one statement and small and medium folders land well inside 100 ms. The very biggest folders still need paging to stay inside the budget. Nothing else is serious.

Judged against:
- Engine: SQLite; sample checked on 3.53.1 (drive.db, README.md). Production version: not stated.
- Size: about 3 million nodes in production, 120,000 in drive.db (README.md). Ran on the sample: 17,958 folders, max depth 53 levels, max 48 children in one folder.
- Folder view: everything under a folder at any depth, `:prefix` ends in `/`, must answer in under 100 ms (README.md, queries/subtree.sql). Interactive.
- Sidebar and header: `queries/children.sql` (one level), `queries/breadcrumbs.sql` (walk up); no budget stated.
- Names: lower-case letters, digits, `-` and `.`, enforced by CHECK, so paths never contain `%` or `_` (README.md, schema.sql).
- Write path (rename, move, create): no code for it in these files; not stated.

## Findings

### critical: `queries/subtree.sql`
LIKE walked into the index, took one look at `:prefix || '%'`, and decided to read all 3 million rows to be safe.
Problem: When the folder view runs `WHERE path LIKE :prefix || '%'` on a 3 million row `node` table, SQLite only turns LIKE into an index range when the right side is a literal or a bound parameter. A concatenation does not qualify (and LIKE is case-insensitive by default, which is a second reason it declines on a plain column). I ran `EXPLAIN QUERY PLAN` on drive.db: `SCAN node USING INDEX sqlite_autoindex_node_1`, even with `PRAGMA case_sensitive_like=1`. Every call reads the whole index. A folder holding 7 rows took 47 ms on the 120k sample (the folder `/web-8/`, 4,375 rows, 53 ms), so the fixed cost alone is about 30 to 45 ms. That scales with table size, so at 3 million rows (25 times larger) a call is roughly 0.8 to 1.2 s before returning a single row (linear extrapolation, not measured). The budget is 100 ms.
Fix: Use a range on the unique `path` index, which `schema.sql` already has:
```sql
SELECT id, path, kind, size_bytes
FROM node
WHERE path >  :prefix
  AND path <  substr(:prefix, 1, length(:prefix) - 1) || '0'
ORDER BY path;
```
`'0'` is the character after `/`, so this is exactly "starts with :prefix" and excludes the folder itself (`path > :prefix`), so the `path <> :prefix` line goes. Verified on drive.db: the plan is `SEARCH node USING INDEX sqlite_autoindex_node_1 (path>? AND path<?)`, the results are identical to the LIKE version for four folders, the 7-row folder drops from 47 ms to 0.1 ms and `/web-8/` from 53 ms to 22 ms. The ORDER BY costs nothing because the index is in `path` order. Do not add another index on `path`: the unique one is enough.

### medium: `folder_view`
Under 100 ms is a promise about the database; shipping 107,000 rows to a browser is a different promise.
Problem: `folder_view` in drive/tree.py returns `fetchall()` of every descendant. After the range fix, the cost is the number of rows returned: on the sample, `/shared-4/q3-reports-20/legal-21/` (39,865 rows) takes about 138 ms and `/shared-4/` (106,766 rows, 89% of the drive) about 340 ms, in Python on this machine. At 3 million rows the largest folders have more. So "big folders" cannot meet 100 ms by indexing alone. Whether the view really has to hand back everything at once is a product decision the README does not settle ("shows everything under a folder, at any depth"), so this is a question to confirm with the UI owner.
Fix: If the UI pages or virtualizes the list, page by key: add `LIMIT :n` to the range query and pass the last path seen as `:prefix` lower bound (`path > :after`) for the next page. Otherwise state the budget as per page.

### low: `path`
A copy of the whole parent chain in every row, with no one in these files minding it.
Problem (question to confirm): `path` repeats what `parent_id` and `name` say, and `queries/subtree.sql` depends on it. That is a legitimate copy, because it serves the stated 100 ms read and is `UNIQUE`. But nothing in these files writes or rewrites it: renaming or moving a folder has to rewrite the `path` of every descendant, and a half-done rewrite makes the folder view and `queries/breadcrumbs.sql` disagree. On drive.db all 120,000 rows agree (I checked `path` against `parent_id` and `name`), so no damage is shown. Where is the write path, and does it change a folder and its descendants in one transaction?
Fix: Make the rename or move one transaction that updates the folder and `UPDATE node SET path = :new || substr(path, length(:old) + 1) WHERE path > :old AND path < substr(:old, 1, length(:old) - 1) || '0'`. If there is no such code yet, nothing to change.

### low: `queries/breadcrumbs.sql`
A walk up the tree with no seatbelt, on a tree that has never needed one.
Problem: `WITH RECURSIVE up ... UNION ALL` has no cycle or depth check, and `schema.sql` does not stop `parent_id` from pointing at a descendant. If a loop ever existed, this query would not finish. The data has none (depth is at most 53 and every row's parent exists), no file moves folders, and each step is a primary key lookup, so as written it is safe. Optional hardening only.
Fix: Optional: add `WHERE u.depth < 100` to the recursive step, or derive the breadcrumb from the `path` string in application code.

## Holds up
- `queries/children.sql`: uses `node_parent(parent_id, name)` (plan: `SEARCH node USING INDEX node_parent (parent_id=?)`, plus a small sort for `ORDER BY kind DESC, name`). The biggest folder has 48 children, the call takes under 1 ms, and the sort only matters if a folder gets thousands of children (not stated). If that happens, make the index `(parent_id, kind, name)`.
- `path` `UNIQUE` (`sqlite_autoindex_node_1`): it is the index the corrected `queries/subtree.sql` uses, and it also guards against duplicate paths.
- `name` CHECK and README note about `%` and `_`: this is why a prefix search needs no escaping. If the name rule is ever relaxed, the range query still works but `/` must stay out of names.
- `node_parent`: used by the `queries/children.sql` lookup; the foreign key does not create an index, and this one covers it.

## Not checked
- Production timings: the 3 million row figures are extrapolated from the 120k sample. A sample shows plan shape and correctness, not speed at that size.
- The SQLite version in production and the write path for rename and move: not stated.
- The Python client's fetch time was included in my timings on this machine; the UI and network time are not.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

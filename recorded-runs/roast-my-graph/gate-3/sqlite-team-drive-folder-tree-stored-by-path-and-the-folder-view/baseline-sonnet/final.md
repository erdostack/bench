The folder view misses its budget because `queries/subtree.sql` can't use the path index, and because it returns every descendant at once. I measured both on drive.db with Python's sqlite3 (SQLite 3.53.1). There is no sqlite3 CLI on this machine. The numbers come from the 120k sample, so the 3M-row figures are extrapolated. Findings are in findings.json.

**What's wrong**
1. **`subtree.sql` does a full table scan.** `path LIKE :prefix || '%'` can't use the unique index on `path`. SQLite's LIKE ignores case but the index compares bytes. The plan is `SCAN node USING INDEX sqlite_autoindex_node_1`, so every folder view reads all nodes. On the sample that is 19-25 ms for a 2.5k-row folder and 270-350 ms for the big ones. At 3M nodes the scan alone should be roughly 25x worse, whatever the folder size.
2. **It returns the entire subtree.** The root and `/shared-4/` return about 120k and 107k rows, and a top-level folder in production could be millions. A faster query can't make that fit 100 ms, and the UI can't show it anyway.
3. **There is no covering index.** Each hit costs a row lookup, because the query reads `kind` and `size_bytes`.
4. **`folder_view` calls `fetchall()` with no limit.** It also binds the caller's prefix to a `LIKE`. The README says names never contain `%` or `_`, but a prefix supplied by a caller can, and it would act as a wildcard.

**What to change**
- **Use a range predicate.** Replace the LIKE with `path >= :prefix AND path < :prefix || char(1114111)`. The plan becomes an index `SEARCH`, and the results are identical to the LIKE version on the four folders I compared. A 4.4k-row folder drops from about 34 ms to about 10 ms. GLOB did not help, because it still scans.
- **Add a covering index.** `CREATE INDEX node_path_cover ON node(path, kind, size_bytes)`. The same folder goes from about 10 ms to about 4.7 ms, and the 107k-row folder from about 0.27 s to about 0.14 s.
- **Paginate.** Use keyset pagination on `path` with `LIMIT 200`. With the range predicate and the covering index, every folder I tried returned its first 200 rows in about 0.2-0.3 ms, including the 107k-row one. `folder_view` should take `limit` and `after` arguments.
- **Order the sidebar query from an index.** `children.sql` needs a temp sort for `ORDER BY kind DESC, name`. An index on `(parent_id, kind DESC, name)` fixes that. It is cheap at today's sizes, so it is low priority.
- **Guard the stored paths.** Nothing enforces that `path` equals the parent's path plus the name. The sample is consistent, but moving or renaming a big folder means rewriting every descendant path. Route those changes through one function or trigger.
- **Leave `breadcrumbs.sql` alone.** It uses primary-key lookups and the deepest path in the sample is 53 levels.

Everything I changed or tested was on a copy in memory, so drive.db and the repo files are untouched apart from the new findings.json.

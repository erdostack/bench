The folder view will not meet 100 ms as written, for two reasons. The query can't use the index on the path, and it returns every row under the folder every time.

What's wrong, most serious first:

1. **The subtree query can't use the path index (queries/subtree.sql, critical).** `path LIKE :prefix || '%'` against the unique index on `node.path` reads the whole table. SQLite only turns LIKE into an index range when the column is NOCASE or case_sensitive_like is on, and neither is set. On the sample, a 554-row folder took about 34 ms with LIKE and about 1.2 ms with a range predicate. Production is about 25 times larger, so expect roughly a second of scanning per request before any rows come back. That is my estimate, not a measurement.

2. **The query returns the whole subtree (queries/subtree.sql, critical).** There is no LIMIT and no keyset. `/shared-4/` has 106,766 rows on the sample. Even with the range fix it takes about 220 ms here, and the same shape at production size is roughly 2.6 million rows. No index can make that fit 100 ms, so the folder view has to be paged.

3. **User input goes straight into the LIKE pattern (drive/tree.py, folder_view, high).** The README's no-`%`-or-`_` guarantee covers stored names, not request paths. `_` matches any character, so `/_hared-4/` matched 106,767 rows on the sample. `/%` matches the whole drive.

4. **fetchall() loads everything into memory (drive/tree.py, folder_view, high).** The cost of a request grows with the size of the folder, not with what the user sees.

5. **Children sort needs a temp sort (node_parent, low).** queries/children.sql orders by `kind DESC, name`, and the index is `(parent_id, name)`, so SQLite sorts each call. Fan-out is small on the sample (max 48), so this is cheap today.

6. **Lower-priority schema points (node.path and node.kind, low).** `path` is a denormalised copy, so a folder move rewrites every descendant path. Nothing enforces that it matches the parent. The sample is consistent. Nothing stops a `doc` node from being a parent, though the sample has none.

What to change, in order:
- Rewrite subtree.sql as a range on the existing index, with keyset pagination and a LIMIT. Compute the upper bound in Python as the prefix with its final `/` replaced by `0`:
  ```
  SELECT id, path, kind, size_bytes FROM node
  WHERE path > :after AND path < :upper
  ORDER BY path LIMIT :page_size;
  ```
  Start with `:after` set to the prefix. Check the plan with EXPLAIN QUERY PLAN. It should show a covering index search with no temp sort.
- Validate the folder path in folder_view (leading and trailing `/`, only `[a-z0-9.-]` segments) and reject anything else.
- Replace fetchall() with one page per request.
- Add the children index `(parent_id, kind DESC, name)`.
- Enforce the parent-path relationship and the no-children-under-docs rule on write.

The timings above come from an in-memory copy of drive.db on this machine, so the absolute numbers are specific to this box. The ratios are what matter. Full list with fixes: /run/work/findings.json

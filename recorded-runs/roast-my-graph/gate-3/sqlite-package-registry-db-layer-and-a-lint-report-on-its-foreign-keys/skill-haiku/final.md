Short answer: the linter is half right, so don't block merges on it as written. The schema alone does not enforce its foreign keys, as the linter says. But this repo never relies on that: `registry/db.py` turns `PRAGMA foreign_keys` on for every connection it opens, and both the cascade and the restrict fired when tested. Nothing serious in the db layer.

- The two `SQLITE-FK-001` errors (schema.sql lines 13 and 14): the rule is right about the DDL alone. A raw connection deleted a depended-on package and left 55 dangling edges. Through `registry/db.py`, unpublishing that package was refused and a leaf's 13 edges were removed. Keep the rule as a warning, or exempt it with a pointer to `registry/db.py` and `test_connections_enforce_foreign_keys`. Add a CI check that `sqlite3.connect` appears only in `registry/db.py`, or move enforcement into triggers if you want it independent of the connection.
- `RECURSIVE-NO-LIMIT` (queries/reverse_deps.sql): a false positive. The recursion carries only `id` under `UNION`, so a synthetic loop still terminated.
- The plan uses `dependency_reverse` for the yank query, which is correct.
- Real but low: `unpublish` reports every integrity error as `StillRequired` and silently accepts an unknown name; `publish` surfaces a self-dependency as a raw database error (rolled back, no bad data).

Not checked: the publish service and CLI are outside this repo, so "nothing else touches the database" is unverified. SQLite version not stated (checked on 3.53.1). `pytest` was not run because it writes outside the working directory; I reproduced the test logic in memory. `registry.db` was opened read-only.

Files: `/run/work/docs/graph/ROAST.md`, `/run/work/findings.json`

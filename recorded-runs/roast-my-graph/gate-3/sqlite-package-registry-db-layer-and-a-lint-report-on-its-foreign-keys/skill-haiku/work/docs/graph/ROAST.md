# Roast: pkgdeps registry (db layer, SQLite)

Verdict: Nothing serious. The linter is half right. Its claim that the schema's foreign keys are not enforced is true of the DDL alone, but the registry never runs the DDL on a connection that skips enforcement: `registry/db.py` turns `PRAGMA foreign_keys` on for every connection, and the cascade and the restrict both fired when run. The `RECURSIVE-NO-LIMIT` warning is a false positive for this query. Blocking merges on the two errors would fail a schema that works, so keep the rule as a warning, or exempt it with a reason, and add a CI check that `sqlite3.connect` appears only in `registry/db.py`.

Judged against:
- Engine: SQLite, from `registry.db` and `registry/db.py` (no version stated in the repo; plans and behaviour checked on SQLite 3.53.1).
- Size: about 6,000 packages and 41,000 edges (`README.md`). Snapshot: 6,000 packages and 39,814 edges (counted).
- Interactive path: the yank dialog runs `queries/reverse_deps.sql` (`README.md`).
- Invariants: unpublishing a package something depends on is refused, and unpublishing removes the package's own dependency rows (`README.md`, `schema.sql`).
- Writers: `registry/packages.py`, reached through `registry/db.py`. The README says nothing else touches the database; this was not checked.

## Findings

### low: `dependency.depends_on_id`
The `ON DELETE RESTRICT` and `ON DELETE CASCADE` clauses in `schema.sql` depend on a connection setting, not on the schema.
Problem: On a connection that does not set `PRAGMA foreign_keys`, the schema enforces nothing. A raw `DELETE FROM package` of a package other packages depend on succeeded on an in-memory copy and left 55 dangling `dependency` rows. Inside the registry this cannot happen, because `registry/db.py` sets the pragma on every connection, and the cascade and restrict both fired (see Holds up). The risk is only a connection opened somewhere else.
Fix: Enforce it in the schema so it does not depend on the connection: a `BEFORE DELETE ON package` trigger that raises when `EXISTS (SELECT 1 FROM dependency WHERE depends_on_id = OLD.id)`, and an `AFTER DELETE` cascade trigger that removes `dependency` rows where `package_id = OLD.id`. Triggers fire whether or not the pragma is on (confirm on the target SQLite version before shipping). Cheaper and sufficient for now: a CI check that `sqlite3.connect` appears only in `registry/db.py`.

### low: `unpublish` (registry/packages.py)
Problem: The `except sqlite3.IntegrityError` catches every integrity error and reports it as `StillRequired`. Today the only integrity error a `DELETE` can raise here is the restrict, so the message is right. Any future constraint on `package` would be reported as a dependency problem.
Fix: Check the dependents explicitly (`SELECT 1 FROM dependency WHERE depends_on_id = ?`) and raise `StillRequired`, or catch only the restrict and re-raise anything else.

### low: `unpublish` (registry/packages.py)
Problem: Unpublishing a name that does not exist deletes nothing and returns `None` with no error. Checked on an in-memory copy: `unpublish(con, "ghost")` returned without raising. A typo in the yank or unpublish dialog looks like success.
Fix: Check `cur.rowcount` and raise `LookupError` when it is 0, inside the same `with con:` block.

### low: `publish` (registry/packages.py)
Problem: A package that lists its own name in `deps` fails at the `dependency` CHECK with a bare `sqlite3.IntegrityError` (`CHECK constraint failed: package_id <> depends_on_id`). The transaction rolls back, so no data is wrong, but the caller gets a database error rather than a clean one.
Fix: Reject `name in deps` before the insert, with a `ValueError`.

### low: `dependency`
Problem: Nothing in the schema stops cycles. Only `publish()` writes edges, and it only adds edges from a new package to existing ones, so none can form today. `reverse_deps` still terminates on a loop, because its `UNION` carries only `id` (checked by adding a two-package loop to an in-memory copy). This is a question, not a defect: if an update-dependencies path is ever added, does a cycle matter for the yank dialog?
Fix: None needed now. If cycles are wanted out, add a check in the write path that the new `depends_on_id` is older than `package_id`, or keep the `UNION` on `id` alone.

## Holds up
- `dependency` PRIMARY KEY `(package_id, depends_on_id)`: serves the forward lookup "what does this package need" by `package_id`. It would stop serving a `depends_on_id` lookup, which the reverse index covers.
- `dependency_reverse (depends_on_id, package_id)`: `queries/reverse_deps.sql` is planned as `SEARCH dependency USING COVERING INDEX dependency_reverse (depends_on_id=?)` on SQLite 3.53.1. It is a covering index seek for the yank dialog's main step.
- `queries/reverse_deps.sql` with `RECURSIVE-NO-LIMIT`: the warning is a false positive. The recursive part carries only `id`, and `UNION` removes repeats, so the walk ends once every package is seen. A loop was added to an in-memory copy and the query returned 5,535 dependents and stopped. The linter's rule should exempt a recursive `UNION` over an id alone.
- `ON DELETE RESTRICT` and `ON DELETE CASCADE` through `registry/db.py`: checked on an in-memory copy. The pragma reads 1 on a `db.connect` connection, unpublishing a depended-on package raised `StillRequired`, and unpublishing a leaf removed its 13 own dependency rows.
- `publish()`: all-or-nothing. A missing dependency and a duplicate name both rolled back, and the package table kept only `core`.
- `CHECK (package_id <> depends_on_id)` on `dependency`: blocks self-dependency at the schema level.
- The linter's `SQLITE-FK-001` errors on `schema.sql:13` and `:14`: the rule is right about the DDL alone (see the first finding) and wrong about this repo, because every connection the code opens enforces the constraints. Keep it as a warning, or exempt it with a pointer to `registry/db.py` and `tests/test_db.py::test_connections_enforce_foreign_keys`.

## Not checked
- The publish service and the CLI are not in this repo. The README says they open the database through `registry/db.py`; this was not confirmed, so the claim that nothing else touches the database is unverified.
- Production size and SQLite version were not stated; plans and behaviour were checked on SQLite 3.53.1 with the snapshot's 6,000 packages.
- `pytest` was not run, because its temporary directories sit outside the working directory; the test assertions were reproduced in memory instead.
- `registry.db` was opened read-only (`mode=ro`), and all write tests ran on in-memory copies. `registry.db` was not changed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

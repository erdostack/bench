# Roast: pkgdeps db layer (schema.sql, registry/, queries/, tests/)

Verdict: Sound, and the linter is wrong. SQLite does not enforce foreign keys by default, but every connection this repo opens does: `registry/db.py` runs `PRAGMA foreign_keys = ON` in its connection class, the README says nothing else opens the database, and `tests/test_db.py` fails if it is off. `ON DELETE CASCADE` and `ON DELETE RESTRICT` fire as the README describes; there is nothing to block a merge on. The findings list is empty.

Judged against:
- Engine: SQLite (README.md); the snapshot was inspected on SQLite 3.53.1. Production version: not stated.
- Size: about 6,000 packages and 41,000 dependency edges (README.md); `registry.db` holds 6,000 packages and 39,814 edges.
- Access: the publish service and the `pkgdeps` CLI both open the database through `registry/db.py`, and nothing else touches it (README.md).
- Guarantees: unpublishing a package that something still depends on is refused (`ON DELETE RESTRICT`); unpublishing removes the package's own dependency rows (`ON DELETE CASCADE`) (README.md).
- Reads: `queries/reverse_deps.sql` answers "what breaks if I yank this?" for the yank dialog (README.md). Write rate: not stated.

## Findings

None.

## Holds up
- `dependency.package_id` and `dependency.depends_on_id` (the foreign keys, `CASCADE` and `RESTRICT`): the linter's `SQLITE-FK-001` is true of a bare SQLite connection and false of this repo. `_Connection.__init__` in `registry/db.py` sets `PRAGMA foreign_keys = ON` on every connection `connect()` returns; `test_connections_enforce_foreign_keys` asserts it; `test_unpublish_refused_while_required` and `test_unpublish_removes_own_edges` only pass with enforcement on, so they exercise both clauses. `unpublish` in `registry/packages.py` turns the resulting `sqlite3.IntegrityError` into `StillRequired`. The snapshot agrees: `PRAGMA foreign_key_check` returns nothing, `PRAGMA integrity_check` returns ok. What would change this: a second way into the database that skips `registry/db.py` (a script, a `sqlite3` shell session). The README says there is none; an exemption for `SQLITE-FK-001` that names `registry/db.py` is the honest way to silence the rule, and that is your call.
- `queries/reverse_deps.sql`: the linter's `RECURSIVE-NO-LIMIT` warning has nothing to catch. The recursive step selects only the id and joins with `UNION` (not `UNION ALL`), so a row seen before is dropped and the walk ends even if a loop existed. There is no loop anyway: `CHECK (package_id <> depends_on_id)` removes self-edges, `publish` can only point a new package at packages that already exist, and a topological sort of the snapshot peels all 6,000 packages. Run on the most depended-on package (55 direct dependents) it returns 5,534 rows in about 60 ms. The plan uses `dependency_reverse` for both the seed and the recursive step.
- `dependency_reverse`: leads with `depends_on_id`, the column `reverse_deps.sql` filters on. The primary key `(package_id, depends_on_id)` serves lookups by `package_id` only, so this index is needed, not redundant.
- `dependency` (table between two packages): both sides are `package`, nothing else references it, and it carries `version_spec`, a property of the pair; one row per pair is the right shape here, not a node.
- `package.name`: `UNIQUE`, which gives it the index `publish`, `unpublish` and `reverse_deps` look up by.
- `publish`: runs in `with con:`, so an unknown dependency (`LookupError`) or a constraint failure rolls back the package row and all edges, as its docstring says.

## Not checked
- Production: the SQLite version, and whether any process other than `registry/db.py` opens the production file.
- Behaviour at write rate: how often packages are published or yanked is not stated; nothing was timed beyond the one read above.
- The linter itself was not run (no network, not installed); its report was read as given. Its line numbers (`schema.sql:13` and `schema.sql:14`) point at the primary key and CHECK lines; the foreign keys are on lines 10 and 11.
- `tests/` was run with pytest against a temporary database: 3 passed. `registry.db` was opened read-only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

**The linter is wrong about the foreign keys. I would not block merges on it.**

SQLite does not enforce FKs by default, so the rule is right in general. It is wrong for this repo. Every connection goes through `registry/db.py`, whose `_Connection` runs `PRAGMA foreign_keys = ON` on open. `tests/test_db.py` asserts that and exercises `RESTRICT` and `CASCADE`, and all 3 tests pass. The linter only reads `schema.sql`, so it cannot see per-connection pragmas. The `registry.db` snapshot is clean: `foreign_key_check` and `integrity_check` pass, and there are no self-edges or cycles. Allowlist `SQLITE-FK-001` with a comment pointing at `db.py` and that test.

The `RECURSIVE-NO-LIMIT` warning on `reverse_deps.sql` is also a false alarm. The CTE uses `UNION`, which discards duplicates, so it terminates even on cyclic data. It also uses the covering `dependency_reverse` index.

**What is actually wrong (8 items in `findings.json`, nothing critical or high):**

- **Thin tests (medium).** There is nothing for publish rollback on an unknown dependency, duplicate names, self-dependency, or `reverse_deps` itself.
- **Bare `pytest` fails (low).** It errors at collection with `No module named 'registry'`. Only `python -m pytest` from the root works, because there is no conftest or pytest config.
- **`publish` error handling is inconsistent (low).** An unknown dependency raises `LookupError`, but a duplicate name or a self-dependency raises a raw `IntegrityError`.
- **`unpublish` on a nonexistent name succeeds silently (low).** Check `rowcount` and raise.
- **FK enforcement depends on convention (low).** Anything that opens `registry.db` without `connect()`, such as the sqlite3 CLI or a script, skips `RESTRICT` and `CASCADE`. Keep `connect()` as the only entry point and add a `foreign_key_check` to CI.
- **`dependency` CHECK is narrow (low).** It forbids only self-edges, not longer cycles. `publish` cannot create cycles, but direct SQL could, and cycle members could never be unpublished.
- **The two linter outputs (medium and low).** Both are false positives and are recorded as findings on the report and on `reverse_deps.sql`, with suppression as the fix.

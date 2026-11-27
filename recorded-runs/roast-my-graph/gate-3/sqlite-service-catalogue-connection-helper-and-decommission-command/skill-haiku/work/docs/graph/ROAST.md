# Roast: svc-catalog (catalog/, schema.sql, tests/)

Verdict: Not ready for other teams. The decommission guard itself works: `depends_on.provider_id` is `ON DELETE RESTRICT` in `schema.sql` and in `catalog.db`, `catalog/db.py` turns foreign keys on, and the four tests pass. But last Friday's `catalog.db` already violates the guard. `PRAGMA foreign_key_check` reports 162 rows in `depends_on`: nine services were deleted while 124 dependency rows still pointed at them, and 38 rows name those same nine as consumers. Fix that data and find the writer that did it before handing out the command. The CLI error paths are a smaller follow-up.

Judged against:
- Guarantee (`README.md`): `svc-catalog decommission <name>` refuses to remove a service that anything still depends on, because `depends_on.provider_id` is `ON DELETE RESTRICT` and every connection turns foreign keys on (`catalog/db.py`).
- Size and use (`README.md`): about 1,800 services and 9,000 dependency edges; `blast-radius` is used by incident commanders during outages.
- Data (`catalog.db`, last Friday's copy, read-only): 1,791 services with ids 1 to 1,800; 8,116 `depends_on` rows; 82 sync and 42 async rows point at deleted providers.
- Schema (`schema.sql`): `depends_on` keyed (consumer_id, provider_id), index `depends_on_provider (provider_id, consumer_id)`, `CHECK (consumer_id <> provider_id)`.
- Engine: SQLite via Python `sqlite3`, version 3.53.1 on this machine (`references/engines.md`; not re-run for this file).

## Findings

### high: `depends_on`
124 `provider_id` values and 38 `consumer_id` values in `depends_on` name ids that are not in `service`. The missing ids are exactly the gaps in 1..1800: 33, 44, 76, 81, 111, 206, 211, 216, 395. The guarantee in `README.md` is false for the stored data.
Problem: 116 existing services still have a dependency on a deleted service, and `BLAST_RADIUS` (`catalog/graph.py`) walks through the deleted ids because its recursive step does not join `service`. When an incident commander runs `blast-radius` on a real service, the result includes services reached only through a deleted one: 120 services' results change when the walk stops at deleted ids, by up to 334 services. The rows are wrong now, and the guard that should have stopped them was not in effect when they were written.
Fix: First find the writer. The rows were created with foreign keys off, so something other than `db.connect` deleted those services (a loader, the `sqlite3` shell, or an older version of the CLI). Then, with each owning team, repoint or remove the 162 rows as a migration (`PRAGMA foreign_key_check` lists them). Make the foreign-key check part of the test run (see `tests/test_graph.py`). Enforce `PRAGMA foreign_keys = ON` for every writer, not only the CLI.

### medium: `tests/test_graph.py`
The four tests pass (`python3 -m pytest`), but they only exercise `catalog.graph` against a three-row in-memory fixture with explicit ids.
Problem: nothing tests the CLI in `catalog/__main__.py`, the shipped `catalog.db`, or referential integrity. That is why the nine deleted services went unnoticed: "tests are green" does not show that the guard holds on the data the other teams will run against.
Fix: add a test that runs `PRAGMA foreign_key_check` on `catalog.db` (read-only) and fails on any row. Add CLI tests for `decommission` (refused, and succeeded on an unused service) and `add-dep` (unknown name).

### low: `main`
Problem: `catalog/__main__.py` catches only `graph.InUse`. `graph.UnknownService`, raised by `service_id` for an unknown name in `decommission`, `add-dep` or `blast-radius`, is not caught, so a typo prints a Python traceback instead of a message.
Fix: catch `graph.UnknownService` in `main`, print the name, and return 1, the same way `InUse` is handled.

### low: `add_dependency`
Problem: every `sqlite3.IntegrityError` becomes `UnknownService`. Checked on an in-memory copy of `schema.sql`: `add_dependency(con, 1, 1)` reports "1 -> 1" as an unknown service, when the real cause is `CHECK (consumer_id <> provider_id)`. A duplicate edge gets the same misleading message.
Fix: check that both ids exist before the insert, and raise a separate error (or re-raise) for CHECK and PRIMARY KEY violations.

### low: `decommission`
Problem: `depends_on.consumer_id` is `ON DELETE CASCADE`, so decommissioning a service silently deletes its outgoing dependency rows. The command prints only "removed", so the team running it cannot see what was deleted. The README does not say this happens.
Fix: count the outgoing rows before the delete and print the number, or confirm with the owners that the cascade is intended.

## Holds up
- `depends_on.provider_id` (`schema.sql`): `ON DELETE RESTRICT`. The guard works for every new delete through `decommission`; `test_decommission_refuses_while_used` covers it. This is why the fix is data, not the schema.
- `graph.decommission` (`catalog/graph.py`): it deletes inside the transaction and turns `IntegrityError` into `InUse` with the dependents listed, then rolls back. Correct for this workload.
- `BLAST_RADIUS` (`catalog/graph.py`): `UNION` keeps one row per service id, so cycles in `depends_on` (only self-loops are blocked) terminate. The recursive step is an index search on `depends_on_provider`.
- `depends_on_provider (provider_id, consumer_id)` (`schema.sql`): leads with the provider column, which is what `dependents` and `BLAST_RADIUS` filter on.

## Not checked
- Which writer deleted the nine services. The files do not show it.
- Whether the 162 rows should be deleted or re-pointed: that needs the owning teams. The fix assumes a migration with owner sign-off.
- The current production `catalog.db`. This is last Friday's copy, read-only. Only the in-memory copy of `schema.sql` was exercised for the error paths.
- Whether a future insert with an explicit id could reuse one of the nine gaps. The `id` column is `INTEGER PRIMARY KEY` without `AUTOINCREMENT`; no file in the repo inserts services with explicit ids outside the tests.
- pytest was run on the repo tests only (4 passed).

Roasted with erdostack: npx skills add usergraphtheory/erdostack

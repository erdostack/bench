# Roast: svc-catalog (catalog/, schema.sql, tests/, catalog.db)

Verdict: Fix `connect` before other teams get `decommission`. The README's guarantee that a service with dependents cannot be removed is false on the connection the CLI really uses, and the green tests do not notice because they use a different connection. I ran `decommission` on a copy of `catalog.db`: it removed a service with 34 dependents and said nothing. The shipped file already has 161 dangling `depends_on` rows, so it has happened. One `critical`, one `medium`, two `low`.

Judged against:
- Engine: SQLite 3.53.1 through Python 3.13 (run here); `pyproject.toml` requires Python 3.12 or newer. The README does not name an SQLite version.
- Size: about 1,800 services and 9,000 dependency edges (README.md); `catalog.db` has 1,791 services and 8,116 `depends_on` rows.
- Guarantees the README relies on: `decommission` refuses to remove a service that anything depends on (`depends_on.provider_id` is `ON DELETE RESTRICT` and `catalog/db.py` turns foreign keys on for every connection); `add-dep` cannot point at a missing service; `blast-radius` lists everything that would break, used by incident commanders during outages (README.md).
- Who writes: the platform team today; other teams soon (your message). Rates and concurrency: not stated.

## Findings

### critical: `connect`
The README promises "foreign keys on for every connection". The connection says "autocommit=False", opens a transaction, and SQLite politely ignores the pragma. It is the only guarantee the system has, and it is a sticky note on a closed door.
Problem: When `svc-catalog decommission <name>` runs on a service that others depend on, it must refuse (README.md). `connect` in `catalog/db.py` opens with `autocommit=False`, which begins a transaction at once, and `PRAGMA foreign_keys = ON` does nothing inside a transaction. I ran it: `PRAGMA foreign_keys` returns 0 on a connection from `connect()`. On a copy of `catalog.db`, `decommission` of `media-notify-0004` (34 dependents) succeeded; dangling rows went from 161 to 198. The shipped `catalog.db` already has 161 `depends_on` rows pointing at missing services (124 with a missing `provider_id`, 38 with a missing `consumer_id`, 9 distinct missing ids). `blast-radius` joins `service`, so removed services drop out of its output during an outage. `add-dep` has the same hole, but the CLI looks both names up first, so it is not the main path.
Fix: In `catalog/db.py` use `sqlite3.connect(path, autocommit=True)`, run `PRAGMA foreign_keys = ON`, then set `con.autocommit = False` (checked here: the pragma then returns 1 and deleting a referenced row raises `IntegrityError`). Add a check that the pragma reads 1 and raise if not. Migration: run `PRAGMA foreign_key_check` on production, decide per row whether to restore the service or delete the row, clean up, then open `decommission` to other teams.

### medium: `con`
Tests green, guarantee broken: the fixture builds its own connection, where the pragma works, and tests that.
Problem: The `con` fixture in `tests/test_graph.py` calls `sqlite3.connect(":memory:")` itself, in the default mode, where `PRAGMA foreign_keys = ON` takes effect. `test_decommission_refuses_while_used` therefore proves the rule on a connection the CLI never uses, and stays green while production has foreign keys off.
Fix: Build the fixture's connection with `db.connect(":memory:")` and load `schema.sql` through it. Add a test that `PRAGMA foreign_keys` returns 1 on a connection from `connect`; it must fail on the current code.

### low: `add_dependency`
Every integrity error is blamed on a missing service, which is a bold theory for a duplicate row.
Problem: `add_dependency` converts any `sqlite3.IntegrityError` into `UnknownService`. Adding a dependency that already exists (primary key), or one on itself (`CHECK`), reports "UnknownService: 1 -> 2". I ran the duplicate case and got that message.
Fix: Distinguish the cases: raise a separate error for an existing dependency and for a self-dependency, and keep `UnknownService` for a missing service.

### low: `main`
Typo a service name and the CLI answers with a stack trace.
Problem: `main` in `catalog/__main__.py` catches `graph.InUse` for `decommission` only. A mistyped name in `decommission`, `add-dep` or `blast-radius` raises `graph.UnknownService` and ends in a traceback, during an outage for `blast-radius`.
Fix: Catch `graph.UnknownService` around all three commands, print "unknown service: <name>" and return 1.

## Holds up
- `depends_on_provider` index on `(provider_id, consumer_id)`: the recursive step in `BLAST_RADIUS`, `dependents` and the `RESTRICT` check all look up by `provider_id`, and the primary key `(consumer_id, provider_id)` only serves `consumer_id`. The index serves them. What would change this: nothing at this size.
- `BLAST_RADIUS` recursive query: `UNION` over the service id alone, so a cycle in the data cannot make it loop (I did not run it for a loop; the data has no two-way dependencies, and `UNION` over one column ends when no new id appears). The service itself would appear in its own radius if a longer cycle existed; nothing in the files says what to do then.
- `ON DELETE CASCADE` on `depends_on.consumer_id`: deleting a service removes the rows saying what it depends on. That is right for decommissioning; only the `RESTRICT` side needs to protect other services, and that is the finding above.
- `service.name` `UNIQUE`, `tier` and `kind` checks, `CHECK (consumer_id <> provider_id)`: the data respects them (`foreign_key_check` is the only constraint that failed on `catalog.db`).
- `decommission` itself: it relies on the database refusing the delete rather than checking first. That is the right design once `connect` really enables foreign keys; an explicit `dependents` check before the delete would be optional insurance.

## Not checked
- Production: only last Friday's `catalog.db` copy was inspected, read-only. The 161 dangling rows are in that copy; production may differ.
- My `decommission` demonstration ran on a throw-away copy of `catalog.db` in a temporary directory, deleted afterwards; `catalog.db` in the repo was not changed.
- Concurrent writers: not stated, not examined.
- Behaviour on Python 3.12 exactly: I ran 3.13. The `autocommit` parameter and the pragma behaviour are the same for the documented transaction rules, but I did not run 3.12.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

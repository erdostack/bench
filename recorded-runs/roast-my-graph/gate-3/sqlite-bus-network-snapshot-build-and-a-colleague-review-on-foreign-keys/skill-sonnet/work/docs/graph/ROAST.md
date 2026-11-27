# Roast: stopgraph (schema.sql, build_snapshot.py, api/)

Verdict: Sound. Nothing needs to change for the foreign key handling: the CRITICAL in docs/review.md does not hold, because the nightly build checks every reference with `PRAGMA foreign_key_check` before publishing, and the API only reads. Keep your day.

Judged against:
- Engine: SQLite (version not stated in the repo; checked here on 3.53.1 via Python sqlite3) (README.md)
- Size: production full load is 3.8M rows; `feed/` and `network.db` are the smaller depot test feed: 1500 stops, 60 routes, 2453 hops (README.md, counted from network.db)
- Writer: one nightly build, `build_snapshot.py`, foreign keys deliberately off during load (40% faster at 3.8M rows), then `PRAGMA foreign_key_check`; any row means the new file is deleted, exit 1, previous `network.db` stays live (README.md, build_snapshot.py)
- Readers: `api/queries.py` opens the published file read-only; nothing else opens it (README.md)

## Findings

None.

I went looking. The schema has no orphans (foreign_key_check on the shipped network.db returns nothing), no self-loop hops, no duplicate (route, from, to), every hop continues from where the previous one on its route ended, and both API queries search by index: `stop.code` unique index, `hop_from`, and for the OR join SQLite uses a MULTI-INDEX OR over `hop_from` and `hop_to`. A database with nothing to roast. Frankly suspicious.

## Holds up
- `build_snapshot.py` / `foreign_key_check`: the guarantee the review wants from `PRAGMA foreign_keys = ON` is provided by the post-load check, which blocks publication of any file with a dangling reference. Enabling the pragma at build time would only slow the 3.8M-row load (README says 40%) to catch the same thing. The pragma is per connection and off by default, but the only writer is the build, and the API never writes, so there is no write for it to guard in the API. Adding it to the API is optional insurance with no effect today. What would change this: a second writer, or the API gaining writes.
- `routes_through`: the review calls the OR join minor; it is fine. The plan is a MULTI-INDEX OR over `hop_from` and `hop_to`, two index searches, not a scan.
- `hop`: a table between `stop` and `route` that is a real edge table: keyed (route_id, seq), carries `minutes`, referenced from both sides; `hop_from` and `hop_to` serve both directions of lookup.

## Not checked
- Production-size timings: only the depot test feed was available, so plan shape was checked, not speed at 3.8M rows.
- Memory of the build at production size: `build_snapshot.py` reads each CSV fully into a list before inserting; not measured, and the README states no memory limit.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

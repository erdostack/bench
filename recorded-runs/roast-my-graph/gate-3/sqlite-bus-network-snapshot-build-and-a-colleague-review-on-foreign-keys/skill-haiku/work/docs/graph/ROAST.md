# Roast: stopgraph (schema.sql, build_snapshot.py, api/queries.py)

Verdict: Sound. Nothing serious: the "CRITICAL" foreign-key claim in docs/review.md does not hold as a defect. Every write path to network.db runs `PRAGMA foreign_key_check` before publishing, the API never writes, and the shipped data has zero dangling references. What is left is six low-severity hardening and clarity items. The foreign-key pragma is not one of them.

Judged against:
- Engine: SQLite syntax and `sqlite3` in build_snapshot.py. Version not stated in the repo. Checked on SQLite 3.53.1 (Python 3.13 `sqlite3`), which is not the production version.
- Size: README says the full load is 3.8M rows and the test feed is smaller. Test feed in feed/: 1500 stop rows, 60 route rows, 2453 hop rows. The 3.8M figure is not checked here.
- Nightly writer: `python3 build_snapshot.py feed/ network.db` (README). Interactive reads: `next_stops` and `routes_through` (api/queries.py). The API opens the file read-only (api/queries.py, `open_ro`; README).
- Invariant: published file only if `PRAGMA foreign_key_check` returns no rows (README step 2; build() in build_snapshot.py).
- docs/graph/CONTEXT.md does not exist. Engine version and production row counts are not stated anywhere else.

## Findings

### low: `hop`
Problem: Foreign key enforcement is off on every connection. hop.route_id, hop.from_stop and hop.to_stop are declared REFERENCES but are not enforced at write time. The only gate is the foreign_key_check in build(), which does not depend on the pragma, and it returns 0 rows on the shipped data. api/queries.py opens the file read-only, so no current path writes an orphan.
Fix: No change needed for correctness. Keep the foreign_key_check gate in build(). Optionally add a test that asserts PRAGMA foreign_key_check returns no rows on the built network.db. Do not turn foreign_keys on in the build: the README records a 40% slower load and the check already covers the same ground.

### low: `build`
Problem: The dangling-reference report prints rowid, but hop is WITHOUT ROWID, so each problem row prints as "hop row None -> stop". Verified in a scratch copy with the extra row 1,99,1,999999,4: the build exits 1 and the message does not identify the row.
Fix: On the failure path only, print the key columns. For hop, select route_id, seq, from_stop, to_stop FROM hop WHERE route_id NOT IN (SELECT id FROM route) OR from_stop NOT IN (SELECT id FROM stop) OR to_stop NOT IN (SELECT id FROM stop) and print those rows.

### low: `build`
Problem: Any load failure other than the FK check raises out of build(). Verified: a hop row with minutes 0 fails CHECK (minutes > 0), the process exits 1 with a traceback, and network.db.new is left on disk. The live network.db is untouched, but the README says a failed build deletes the new file, and that holds only for the FK path.
Fix: Wrap the load and check in try/except that unlinks the .new file and then re-raises or returns 1, so every failure leaves the same state.

### low: `hop`
Problem: The comment in schema.sql says there is one hop per pair of consecutive stops on a route's pattern, but nothing enforces the chain (to_stop of seq n equals from_stop of seq n+1) or that from_stop differs from to_stop. The shipped data has 0 chain breaks and 0 self-loops across 2453 rows, so this is a question to confirm, not a live defect.
Fix: Confirm with the feed owner whether a chain break or self-loop is ever legal. If not, add CHECK (from_stop <> to_stop) to hop in schema.sql and add a query-based chain check to build() that fails the build like the foreign_key_check gate.

### low: `build`
Problem: build() interpolates CSV header names directly into the INSERT statement, and an empty feed file fails with IndexError on rows[0]. The feed is trusted and the headers are fixed today, so this is hardening only.
Fix: Compare each CSV header with the expected column list for its table before inserting, and fail with a clear message on a mismatch or an empty file.

### low: `stop`
Problem: 262 of the 1500 rows in stop appear in no hop row, so next_stops and routes_through return nothing for them. This may be correct for a depot test feed, but the files do not say so.
Fix: Confirm with the feed owner whether those stops are meant to be unserved. If they should be served, the feed export is dropping their hops. If not, add a README line saying the feed carries unserved stops.

## Holds up
- `hop` (PRIMARY KEY (route_id, seq), WITHOUT ROWID): the key leads with route_id, so per-route pattern reads are a search. Would change if a lookup by seq alone appeared.
- `hop_from` and `hop_to`: both directions of next_stops and routes_through have an index. The routes_through OR join plans as MULTI-INDEX OR over both indexes, so the review's "Minor" note is not a cost on this data.
- `stop.code` (UNIQUE): the index that next_stops and routes_through use to find a stop by code. Plan is SEARCH USING COVERING INDEX.
- build() foreign_key_check: works without PRAGMA foreign_keys, so it catches dangling hops in the nightly build. Confirmed: a dangling hop row produces exit 1 and no network.db.new is published.
- The API is read-only (`mode=ro`), so no API path can introduce an orphan.

## Not checked
- Production scale (3.8M rows) and the README's 40% figure: only the 2453-row test feed was loaded and timed. No timing was measured.
- The SQLite version in production: not stated. Results are from SQLite 3.53.1.
- The review's claim that orphaned edges "corrupt routing" was not reproduced through the API, since the API cannot write.
- Whether the 262 unserved stops are intended.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

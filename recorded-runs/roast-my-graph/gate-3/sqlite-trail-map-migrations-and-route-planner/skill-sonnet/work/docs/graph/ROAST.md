# Roast: trail map repo (migrations/, migrate.py, trailmap/, trails.db)

Verdict: Nothing sound about the one guarantee the README brags about: closed junctions are not removed from the map, and `route()` walks hikers straight through them today. One critical, one low, the rest is fine.

Judged against:
- SQLite (3.53.1 via Python 3.13 `sqlite3`, the one I ran); engine version of the live deployment: not stated.
- About 900 junctions and 1,400 segments; `trails.db` holds 896 `junction` rows and 1,388 `segment` rows (README.md, checked against the db copy).
- `close_junction` is used when rangers close a bridge or junction; README says it "also removes every segment that touches it, and the planner can never send anyone through a closed junction" (README.md).
- `route()` serves the kiosk at each trailhead and the web page: interactive, every request (README.md).
- Write rate, number of writers, engine access: not stated.

## Findings

### critical: `close_junction`
The README promises a cascade. The database never got the memo. `PRAGMA foreign_keys` is a per-connection switch, and the only place that flips it is a script run by `migrate.py` on a connection that is closed seconds later. Every later connection starts with it off, so `ON DELETE CASCADE` is a decorative comment with a SQL accent, and the planner is happily marching tourists across a bridge the rangers closed. Seven segments point away from nothing and eight point to nothing. Nobody is going to be mad at the schema for this. The schema was told the lights were on.
Problem: When `close_junction` runs `DELETE FROM junction WHERE code = ?` on a connection from `connect_db` (foreign keys off), no segment is removed. The shipped `trails.db` already shows it: `PRAGMA foreign_key_check` reports 15 orphan segment rows (ids 326, 369, 371, 372, 624, 626, 665, 667, 668, 669 and others) that touch the deleted junction ids 248, 433, 434 and 681, and `PRAGMA foreign_keys` reads 0 on a fresh connection. `route()` reads every row of `segment`, so on the copy `route(con, 'J0220', 'J2008')` returned 17325 m through the closed junction (printed as `'433'`, because `codes.get(j, str(j))` falls back to the raw id), and `J0220` to `J2409` and `J0620` to `J2008` do the same. This is the one thing the README says can never happen.
Fix: (1) In `connect_db` run `con.execute("PRAGMA foreign_keys = ON")` right after `sqlite3.connect(path)`, since the setting is per connection and `PRAGMA foreign_keys = ON` in `migrations/001_init.sql` only covers the migration run. (2) Clean the stored orphans with a new migration `migrations/003_remove_orphan_segments.sql`: `DELETE FROM segment WHERE from_junction NOT IN (SELECT id FROM junction) OR to_junction NOT IN (SELECT id FROM junction);` (3) Check with `PRAGMA foreign_key_check;` (should return no rows) and rerun `route()` on the three pairs above. Stopgap only, if the connection change cannot ship at once: have `route()` skip segments whose endpoints are not in `ids`; that hides the symptom and leaves orphans stored.

### low: `add_segment`
Ask it to connect a code that does not exist and it shrugs: the `INSERT ... SELECT ... FROM junction a, junction b WHERE a.code = ? AND b.code = ?` matches zero rows, inserts nothing and raises nothing.
Problem: Question to confirm, not a proven defect: when `add_segment` is called with a misspelled junction code, no segment is added and the caller is not told. Nothing in the files shows this happening.
Fix: Check `cursor.rowcount` after the `execute` and raise `ValueError` when it is 0.

## Holds up
- `segment_from` and `segment_to`: both directions are searched in a graph that is walked both ways, and SQLite does not create an index for a foreign key; at 1,388 segments `route()` reads the whole table once anyway, so they cost little and break nothing.
- `route`: a plain Dijkstra with a heap and a stale-entry check, edges added in both directions to match "trails can be walked both ways". Reading all 1,388 segments per call is fine at the stated 900 junctions and 1,400 segments. Its only problem is the stored orphans above; it computes the right thing on clean data.
- `junction.code`: `UNIQUE`, which is the key every function looks up by.
- `segment` CHECK constraints (`length_m > 0`, `difficulty`, `surface`, `from_junction <> to_junction`): the data shows no violations, and `surface` migrated cleanly through `migrations/002_surface.sql`.
- `segment` stored once per trail: no pair appears twice in either direction, so there is no mirrored-row duplication.
- `migrate.py`: applies scripts in order by `PRAGMA user_version`; database is at version 2 matching both migrations.

## Not checked
- The live deployment's other connections and writers (kiosk, web page): their code is not in the repo, so I could not see how they open the database.
- Whether the 15 orphan rows are all closures that rangers intended: the files do not say, so the cleanup in fix step 2 assumes yes; confirm with the rangers' closure list.
- Runs were on a copy of `trails.db` in `/tmp`; the original was only opened read-only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

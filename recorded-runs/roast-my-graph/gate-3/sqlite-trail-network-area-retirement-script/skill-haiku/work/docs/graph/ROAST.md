# Roast: trailplan route planner and retire_area.py

Verdict: Not sound. Closing the quarry failed. `scripts/retire_area.py` never turns on SQLite foreign keys, so the `ON DELETE CASCADE` on `segment` didn't run, and the planner still routes through the 60 retired junctions. In trails.db, 90 segments point at junction ids that no longer exist, and 192 of 399 random routes between live junctions pass through one of them. The fix is one line in the script plus a one-off migration.

Judged against:
- Engine: SQLite (trails.db, schema in db/schema.sql). The engine notes give SQLite 3.53.1 with `PRAGMA foreign_keys` off on a new connection (engines.md).
- Declared intent: when an area closes, its junctions are deleted and its segments go with them (README.md, scripts/retire_area.py docstring).
- Retirement record: `retired_area` holds `quarry`, 2026-09-12, reason `blasting` (trails.db).
- Foreign keys: `segment.from_junction` and `segment.to_junction` reference `junction (id) ON DELETE CASCADE` (db/schema.sql).
- Connection setup: `app/db.py` turns the pragma on; `scripts/retire_area.py` calls `sqlite3.connect(DB)` directly (both files).
- Size: 300 junctions, 519 segments, five areas of 60 junctions each in the sample (trails.db). Production size not stated.

## Findings

### critical: `retire`
Problem: `retire()` opens its own connection with `sqlite3.connect(DB)` and never runs `PRAGMA foreign_keys = ON`. SQLite leaves foreign keys off by default, so the `ON DELETE CASCADE` on `segment` never fires and the quarry's segments stay behind. Re-running the same DELETE on a copy of trails.db for one area (`summit`) left 177 dangling segments with the pragma off; with it on, the count stayed at the 90 already there, so the cascade added none.
Fix: Open the connection through `app.db.connect()`, or run `con.execute("PRAGMA foreign_keys = ON")` right after `sqlite3.connect(DB)`.

### critical: `segment`
Problem: The damage is already in the data. 90 rows reference junction ids that no longer exist (the quarry's 60 junctions). `load_graph` reads every segment, and in a random sample of 399 routable pairs between live junctions, 192 shortest routes passed through a retired id.
Fix: Run once: `DELETE FROM segment WHERE from_junction NOT IN (SELECT id FROM junction) OR to_junction NOT IN (SELECT id FROM junction);`. Then keep the cascade working for every writer, with the pragma fix above. If other code can write to `junction`, add `CREATE TRIGGER junction_cascade AFTER DELETE ON junction BEGIN DELETE FROM segment WHERE from_junction = OLD.id OR to_junction = OLD.id; END;`. The trigger is SQLite syntax; it was not run here.

### medium: `plan`
Problem: `names.get(j, f"junction {j}")` puts a placeholder into the route for any junction id with no row, and no error is raised. A route through the closed quarry reads as an ordinary list of stops ("junction 169"), which hides the dangling segments from anyone reading the output.
Fix: Check that every id in the path is in `names` and raise an error naming any that are missing. Keep the placeholder only for display once the migration and the pragma fix are in.

### medium: `load_graph`
Problem: `nx.Graph` plus `add_edge(a, b, metres=metres)` keeps only one segment per pair, and the last one read wins. Six pairs in trails.db have two segments. For junctions 193 and 194, 1183 m is kept where 473 m also exists, and the same happens for 302 and 303 and for 319 and 320. The schema has no uniqueness rule on the pair, so the file does not say whether the duplicates are real trails or data errors. In the 1,770 live-junction pairs compared, the total length did not change, so this is a wrong distance rather than a wrong route so far.
Fix: Build `nx.MultiGraph()` instead. With `weight="metres"`, `shortest_path` then uses the smallest parallel segment; checked on trails.db, a MultiGraph gives 586 m for junctions 16 and 17, the minimum of the two. Confirm with the park whether the longer duplicates should be deleted.

## Holds up
- `segment_from` and `segment_to`: serve the cascade lookups and the foreign-key checks once they are enabled.
- `junction_area`: serves the `DELETE ... WHERE area = ?` in `retire()`.
- `CHECK (metres > 0)`: no zero or negative weights, so Dijkstra's assumption holds for `shortest_path`.
- `ON DELETE CASCADE` as declared: with the pragma on, the sample's `summit` area retired cleanly, with 60 junctions removed and no new dangling segments. The schema is correct; the connection is not.
- `retired_area`: an audit record keyed by area. The planner does not read it, which is fine as long as the junctions and segments are actually removed.

## Not checked
- `scripts/retire_area.py` was not run against trails.db, because it writes. Its statements were run on in-memory copies with the same connection settings: pragma off gave 177 dangling segments after closing `summit`, pragma on gave 0 new.
- `plan()` itself was not called, because it connects to `trails.db` in the working directory. Its routing was reproduced with the same `load_graph` code on a read-only connection.
- Whether real rangers' routes went through the quarry is not in the files. The sample shows the same mechanism working on this data.
- Whether the duplicate segments are real separate trails is not stated.
- Production size is not stated.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

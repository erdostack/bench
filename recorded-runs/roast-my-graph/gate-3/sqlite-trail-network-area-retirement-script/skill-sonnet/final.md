Your retire script is why the planner sent a group through the quarry. It is critical, and the bad data is in trails.db now.

`scripts/retire_area.py` relies on `ON DELETE CASCADE`, but it opens its own `sqlite3.connect` and never runs `PRAGMA foreign_keys = ON`. Only `connect` in app/db.py does that, and SQLite has foreign keys off by default on each connection. So the junction rows were deleted and the cascade never fired. In trails.db the quarry has no junctions, but 90 of its segments are still there (`PRAGMA foreign_key_check` reports 174 violations). Six of them (segment ids 508 to 513) connect live junctions to the quarry corridor. In a sample of 3,000 random start and end pairs, 1,462 routes ran through a deleted junction. The script printed success, and `plan` hides the missing junctions with `names.get(j, "junction N")`, so nothing raised an error.

What to change:
1. In `retire`, use `app.db.connect` or set the pragma, and delete the segments explicitly in the same transaction.
2. Back up trails.db, then delete the orphan segments: `DELETE FROM segment WHERE from_junction NOT IN (SELECT id FROM junction) OR to_junction NOT IN (SELECT id FROM junction);`. Then `PRAGMA foreign_key_check` should be empty. Run the same check on production and on any other area retired with this script.
3. Closing the quarry correctly splits the sample network in two: north-ridge with lakeside, and old-forest with meadows and summit. About half of start and end pairs will have no route, and `plan` doesn't catch `NetworkXNoPath`, so it will raise. Handle that, and ask the rangers whether other trails join the two parts and are missing from `segment`.
4. In `load_graph`, join `junction` on both ends so a missing junction can never be loaded.
5. In `load_graph`, `nx.Graph` keeps the last row when two segments join the same pair of junctions, not the shortest. Six pairs are affected, and in three of them the longer row wins. Keep the shortest.
6. Low, a question to confirm: `retire` records a mistyped area as retired when it matches no junctions.

I could not check production. Only trails.db was examined, read-only.

Files are in the repo root, and the full roast is at docs/graph/ROAST.md:
- findings.json
- docs/graph/ROAST.md

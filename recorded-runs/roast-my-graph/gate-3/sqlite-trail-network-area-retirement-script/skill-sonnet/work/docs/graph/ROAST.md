# Roast: trailplan (db/schema.sql, scripts/retire_area.py, app/, trails.db sample)

Verdict: Yes, your retire script is why the planner routed a group through the quarry. `scripts/retire_area.py` relies on `ON DELETE CASCADE` but never turns foreign keys on, so SQLite deleted the quarry's junctions and left all 90 of its segments in place, and the planner still walks them. This is critical and live in trails.db right now.

Judged against:
- Engine: SQLite (trails.db, checked read-only on 3.53.1). Production version: not stated.
- Closing an area: `python scripts/retire_area.py <area>`; "its junctions are deleted and the segments go with them" (README.md, the script's docstring). Done "like always": the cascade is the stated mechanism.
- Routing: `plan` loads every segment and runs `nx.shortest_path(..., weight="metres")` on each request (app/routes.py). Size: 300 junctions, 519 segments in the sample; production size and request rate: not stated.
- Sample state: `retired_area` has `quarry`, retired 2026-09-12, reason blasting; no `quarry` junction rows; 60 junctions per live area in 5 areas.
- Where foreign keys get switched on: `connect` in app/db.py only. `PRAGMA foreign_keys` is off on a new SQLite connection and is per connection.

## Findings

### critical: `scripts/retire_area.py`
The script says "segments go with them" the way a landlord says "the tenants will be out by Friday": it never checked anyone was told.
Problem: `retire` opens `sqlite3.connect(DB)` directly, not `connect` from app/db.py, and never runs `PRAGMA foreign_keys = ON`. With the pragma off, `DELETE FROM junction WHERE area = ?` removes the junction rows and the `ON DELETE CASCADE` on `segment.from_junction` and `segment.to_junction` never fires. In trails.db the `quarry` area has no junctions and 90 of its segments (ids 169 and up, junctions 121 to 238) are still there; `PRAGMA foreign_key_check` reports 174 violations. The script prints "retired quarry: N junctions" and commits, so nothing looks wrong.
Fix: Open the database with the app's `connect` (`from app.db import connect`; run from the repo root with `python -m scripts.retire_area` or add `scripts/__init__.py`), or at least run `con.execute("PRAGMA foreign_keys = ON")` before the DELETE. Better, delete the segments explicitly in the same transaction so the result does not depend on a per-connection setting: `DELETE FROM segment WHERE from_junction IN (SELECT id FROM junction WHERE area = ?) OR to_junction IN (SELECT id FROM junction WHERE area = ?)` before the junction delete.

### critical: `segment`
Ninety trail sections that lead to nowhere, and six that lead from somewhere real into nowhere.
Problem: The rows left by the failed cascade are in `segment` now: 90 segments reference junction ids that no longer exist (121 to 180 and others; 60 ids total), and 6 of them (ids 508 to 513, for example 508 from junction 77 to 165) have one end on a live junction. These six are the entry and exit of the quarry corridor, so the planner sends people into it. In a sample of 3,000 random start and end pairs, 1,462 of the shortest routes ran through a deleted junction. The quarry was closed for blasting.
Fix: Delete the orphans now, in a transaction, after backing up trails.db: `DELETE FROM segment WHERE from_junction NOT IN (SELECT id FROM junction) OR to_junction NOT IN (SELECT id FROM junction);` then `PRAGMA foreign_key_check;` must return nothing. Check the area list in `retired_area` against any other area retired the same way. Note what this changes: with the quarry gone, the live network splits into two parts (north-ridge with lakeside, 120 junctions; old-forest, meadows and summit, 180 junctions). The quarry corridor was the only link between them in this sample. See `plan`.

### medium: `load_graph`
It trusts every segment row, like a taxi driver who believes every road the map ever showed.
Problem: `load_graph` builds the graph from `SELECT from_junction, to_junction, metres FROM segment` alone and adds every endpoint it sees, so a segment whose junction is gone becomes a node in the route. `plan` then hides it with `names.get(j, f"junction {j}")`, which is why a rangers' report said "quarry" and no one saw an error in the code. Once `scripts/retire_area.py` and the data are fixed the orphans cannot exist, so this is the second line of defense.
Fix: Join `junction` on both ends in the query (`FROM segment s JOIN junction a ON a.id = s.from_junction JOIN junction b ON b.id = s.to_junction`) so a segment with a missing end is never loaded, and let `plan` use `names[j]` rather than a fallback that prints raw ids.

### medium: `load_graph`
Two trails between the same junctions, and the graph keeps whichever row came last.
Problem: `nx.Graph.add_edge` overwrites an existing edge. Six junction pairs in `segment` have two rows (for example 193-194: segment 265 with 473 m and segment 313 with 1183 m; 302-303: 422 with 410 m and 490 with 786 m; 319-320: 439 with 594 m and 483 with 1291 m). For these three the last row is the longer one, so `nx.shortest_path` is run on a distance that is not the shortest, and routes and totals over those junctions are longer than they should be. The files do not say the pairs are different trails with a reason to prefer the longer one.
Fix: Keep the shortest per pair: `if G.has_edge(a, b) and G[a][b]["metres"] <= metres: continue` before `add_edge`, or use `nx.MultiGraph`, for which `shortest_path` takes the lightest parallel edge. Confirm with whoever owns the data that the duplicates are real alternatives and not entry mistakes.

### medium: `plan`
Closing the quarry correctly will cut the park in two, and this function will answer with a stack trace.
Problem: After the orphans are removed, 120 and 180 junctions are in separate components (see `segment`), so about half of the start and end pairs have no route, and `nx.shortest_path` raises `NetworkXNoPath` (and `NodeNotFound` for an unknown id). `plan` does not catch either. Today the quarry bridges the gap, which is the bug. The fix is correct and will expose this.
Fix: Catch `nx.NetworkXNoPath` and `nx.NodeNotFound` in `plan` and return "no open route" to the caller. Ask the rangers whether other trails join the two parts and are missing from `segment`.

### low: `retire`
A typo is a successful retirement.
Problem (question to confirm): `retire` inserts into `retired_area` and prints success even when the DELETE matched zero junctions (`retire_area.py quary` records an area that does not exist). Nothing in the files shows it happening.
Fix: Exit with an error when `n == 0`, or when the area is not in `junction` and not already in `retired_area`.

## Holds up
- `ON DELETE CASCADE` on `segment` and the `retired_area` table: right design for the README's "junctions deleted, segments go with them", and `connect` in app/db.py does switch foreign keys on. It only fails for a connection that does not use `connect`.
- `junction_area`, `segment_from`, `segment_to`: the delete and the cascade search by these columns, so they are all used; sizes are small.
- `junction` and `segment` as tables with `from_junction` and `to_junction` both indexed: right for a trail graph, no extra table in between.
- `load_graph` reading the whole graph on every call: 519 segments in the sample. Production size and rate are not stated; only a cost if the network is much larger.

## Not checked
- Production data and the other areas retired before the quarry: only trails.db was examined, read-only. Run `PRAGMA foreign_key_check` on production.
- Whether the six duplicate segment pairs are real alternatives.
- How the app calls `plan` and handles errors: only app/routes.py is in the files.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

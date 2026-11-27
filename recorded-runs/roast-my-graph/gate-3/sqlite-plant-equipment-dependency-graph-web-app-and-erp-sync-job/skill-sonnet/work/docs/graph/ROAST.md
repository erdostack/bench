# Roast: plant equipment db (app/, jobs/, db/, plant.db)

Verdict: The nightly ERP sync has been leaving dead equipment behind in the dependency tables, and the planners' "what stops if this fails" page shows it. `jobs/sync_from_erp.py` relies on `ON DELETE CASCADE` but never switches foreign keys on, so decommissioned equipment is deleted and its `depends_on` and `installed_in` rows stay. The copy of `plant.db` already has 1,322 such orphan rows, and I measured wrong impact lists for 817 of 2,860 pieces of equipment.

Judged against:
- Engine: SQLite (`README.md`); version not stated. Checked on SQLite 3.53.1 through Python 3.13 here.
- Sizes (from the morning copy `plant.db`, not the README): 2,860 `equipment`, 7,000 `depends_on`, 900 `installed_in`. The README gives no counts; it says a few hundred pieces are decommissioned a year.
- Operations: the planners' app runs `impact.sql` ("what stops if something fails") and `dependency_counts.sql` (top 20 most depended-on equipment); the ERP sync runs nightly, inserting new equipment and deleting decommissioned equipment (`README.md`). Traffic: not stated.
- Writers: `jobs/sync_from_erp.py` (`sqlite3.connect`, no pragma) and the app (`app/db.py`, `PRAGMA foreign_keys = ON`); the sync's comment says the delete is relied on to cascade.
- Constraints: `equipment.tag` UNIQUE; foreign keys with `ON DELETE CASCADE` on `depends_on` and `installed_in`; `depends_on` primary key `(src_id, dst_id)` plus index `depends_on_dst (dst_id, src_id)` (`db/schema.sql`).

## Findings

### critical: `sync`
The schema promises a cascade. The job that does the deleting never asked SQLite to keep that promise, so every decommissioned pump leaves a ghost that other equipment still depends on.
Problem: `sync` opens its own connection with `sqlite3.connect(db_path)` and never runs `PRAGMA foreign_keys = ON` (it is off on every new connection; only `app/db.py` turns it on). So `DELETE FROM equipment WHERE tag = ?` for each decommissioned row does not cascade, and the `depends_on` and `installed_in` rows pointing at the deleted id stay. On the shipped copy `PRAGMA foreign_key_check` returns 1,322 violations: 571 `depends_on.src_id`, 619 `depends_on.dst_id`, 78 `installed_in.part_id` and 54 `installed_in.assembly_id` values point at 260 or so equipment ids that no longer exist.
Fix: Turn foreign keys on, outside any transaction, right after connecting (a no-op inside one):
```
con = sqlite3.connect(db_path)
con.execute("PRAGMA foreign_keys = ON")
```
Then clean what is already stored, once, in one transaction, and check it:
```
DELETE FROM depends_on  WHERE src_id NOT IN (SELECT id FROM equipment) OR dst_id NOT IN (SELECT id FROM equipment);
DELETE FROM installed_in WHERE part_id NOT IN (SELECT id FROM equipment) OR assembly_id NOT IN (SELECT id FROM equipment);
PRAGMA foreign_key_check;   -- must return no rows
```
Optionally have `sync` run `PRAGMA foreign_key_check` at the end and fail loudly if it returns rows. Take a backup first, and run the cleanup on the production file, not only the copy.

### critical: `impact.sql`
It tells a planner that things will stop because of equipment that was scrapped.
Problem: When a planner runs `impact.sql` for a piece of equipment that has orphan `depends_on` rows in its dependency chain, the recursive step `JOIN hit ON d.dst_id = hit.id` follows edges that run through deleted equipment ids, so live equipment appears in "everything that stops" only because it depended on something that no longer exists. I ran it on the copy with and without the orphan rows: results differ for 817 of 2,860 equipment ids, with 10,527 extra rows in total, worst case equipment id 238 returning 193 rows instead of 82. (The final join to `equipment` hides the deleted ids themselves, so the list looks plausible.) The recursion itself terminates on loops, since `UNION` over rows carrying only the id de-duplicates.
Fix: The fix is the `sync` change and one-off cleanup above; the query itself is right once the data is. If you want a guard that survives future drift, join `equipment` inside the recursive step (stopgap): `SELECT d.src_id FROM depends_on d JOIN hit ON d.dst_id = hit.id JOIN equipment s ON s.id = d.src_id JOIN equipment t ON t.id = d.dst_id`.

### high: `dependency_counts.sql`
Counts the dead as dependants, so the top-20 list is quietly inflated.
Problem: When the planners open the most-depended-on list, `count(*)` over `depends_on` counts rows whose `src_id` is a deleted equipment id as dependants of live equipment, and rows whose `dst_id` is deleted are dropped by the join. On the shipped copy the output differs from the cleaned data: for example `EQ-00252` shows 13 dependants where 11 are real, and the order of the top entries changes (`EQ-00198` should lead).
Fix: Same cause, same fix: run the `sync` change and cleanup. After that no query change is needed; as a stopgap join the source side too: `JOIN equipment s ON s.id = d.src_id`.

## Holds up
- `depends_on_dst` and the primary key `(src_id, dst_id)`: `impact.sql` walks dependants by `dst_id` (plan: `SEARCH d USING COVERING INDEX depends_on_dst`), and `equipment` is read by integer primary key. Both directions are indexed.
- `dependency_counts.sql`: a full scan of 7,000 rows for a top 20 is fine at this size.
- `impact.sql` termination: `UNION` on a one-column recursive row means a dependency loop would not run forever.
- `equipment.tag` with `ON CONFLICT (tag) DO UPDATE`: `tag` is the ERP key and unique, so the nightly upsert matches the same equipment each time.
- `app/db.py`: sets `PRAGMA foreign_keys = ON`, so the app's own writes would cascade; the gap is only the job.

## Not checked
- I ran everything read-only against the morning copy (opened with `mode=ro`, results compared in an in-memory copy); the production file at `/srv/plant/plant.db` may differ.
- Whether any equipment id was reused after a delete (SQLite can hand out a deleted maximum `id` again, which would attach old orphan rows to new equipment) is not visible in the copy: no orphan id is above the current maximum.
- Traffic and row counts beyond the copy: not stated.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

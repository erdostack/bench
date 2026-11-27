# Roast: plant equipment db (app/, jobs/, db/)

Verdict: Not sound. The nightly ERP sync deletes decommissioned equipment without turning on foreign keys, so the cascade the code comment relies on never runs. The copy from this morning already has 1,322 broken references, and both planner queries read them: the impact list walks through pieces that no longer exist (180 of 200 sampled equipment), and the most-depended-on list counts dependants that are gone (6 of the top 20 change).

Judged against:
- SQLite. `equipment` holds every pump, motor, valve, sensor and panel; `depends_on` says one piece needs another to run; `installed_in` says which assembly a part sits in. (README.md)
- A few hundred pieces are decommissioned a year, and the nightly job removes them. (README.md)
- Planners' app shows what stops if something fails (`db/impact.sql`) and which equipment the most things depend on (`db/dependency_counts.sql`). (README.md)
- The sync comment says the decommissioned piece's `depends_on` and `installed_in` rows "go with it (ON DELETE CASCADE)". (jobs/sync_from_erp.py, line 16)
- Measured on plant.db (copy from this morning, opened read-only): 2,860 equipment, 7,000 depends_on, 900 installed_in. Row counts are not stated in the README; these are measured. Equipment ids run to 3120, so about 260 have been removed.
- Interactive: the two planner queries and `app/db.py`. Batch: the nightly sync. No size or rate stated for the planner views.

## Findings

### critical: `sync`
The job deletes a piece, the schema is ready to tidy up after it, and the one switch that makes it happen is left off, so every decommissioning leaves a little ghost behind.
Each decommissioned tag is deleted with `DELETE FROM equipment WHERE tag = ?` on a connection that never runs `PRAGMA foreign_keys = ON`. SQLite leaves that off on a new connection, so the `ON DELETE CASCADE` on `depends_on` and `installed_in` never fires.
Problem: On plant.db today, `depends_on` has 571 rows whose `src_id` is gone and 619 whose `dst_id` is gone, and `installed_in` has 78 dangling parts and 54 dangling assemblies. `PRAGMA foreign_key_check` reports 1,322 violations. Every decommissioned piece leaves its links behind, and the planner queries read them.
Fix: Turn foreign keys on for the sync connection before any write (it cannot change inside a transaction, and the `with con:` block opens one on the first write). Clean up what is already stored, then enforce from now on:
```python
con = sqlite3.connect(db_path)
con.execute("PRAGMA foreign_keys = ON")
```
Migration, run once in the same transaction before the loop:
```sql
DELETE FROM depends_on WHERE src_id NOT IN (SELECT id FROM equipment)
                          OR dst_id NOT IN (SELECT id FROM equipment);
DELETE FROM installed_in WHERE part_id NOT IN (SELECT id FROM equipment)
                            OR assembly_id NOT IN (SELECT id FROM equipment);
```
Also check `PRAGMA foreign_key_check` returns no rows after the run. The copy is read-only and was not changed here.

### high: `db/impact.sql`
The planners asked what stops when a pump fails and the answer includes equipment that was scrapped last spring, which is a lot of worry for a dead pump.
The recursion follows `depends_on` from `dst_id` to `src_id` and only checks the id, so it goes through ids that are no longer in `equipment`. The final `JOIN equipment` drops them from the output but not from the walk.
Problem: When `:equipment_id` is anything with dependants, the walk carries on through removed pieces and reports equipment that reaches the failed piece only through a removed one. In a sample of 200 alive equipment, 180 walks passed through at least one id not in `equipment`. Those are over-reports for the planners, not missed failures.
Fix: Removing the dangling rows (the `sync` fix) is the cause fix. As a stopgap until then, add `JOIN equipment s ON s.id = d.src_id` to the recursive step and `JOIN equipment dn ON dn.id = d.dst_id` so the walk stops at removed pieces.

### high: `db/dependency_counts.sql`
It joins `equipment` only on `dst_id`, so it counts dependants that are gone.
Problem: The count for each equipment includes `depends_on` rows whose `src_id` was decommissioned. On plant.db the top-20 list changes: EQ-00252 shows 13 where 11 is correct, and six tags in the top 20 move out. The ordering the planners see is wrong today.
Fix: The `sync` fix removes the stale rows, so this is correct afterwards. As a stopgap, add `JOIN equipment s ON s.id = d.src_id` before the `GROUP BY`.

### low: `installed_in`
No query in `app/` or `db/` reads this table, although the README says it says which assembly a part sits in.
Problem: The table is stored, enforced through the same broken cascade (the 78 and 54 dangling rows above), and read by nothing in this repo. Either the planners use it elsewhere or it is dead weight.
Fix: Confirm whether anything outside this repo reads it. If nothing does, drop it; if something does, fix it with the `sync` change.

### low: `sync`
The upsert is keyed on `tag` alone, so a piece whose ERP tag changes gets a second row and the old one stays until it is decommissioned.
Problem: Nothing in the files says whether tags are permanent. If they can be renamed in ERP, the same piece appears twice.
Fix: Confirm that tags are permanent in the ERP export. If they can change, key on an ERP id instead.

## Holds up
- `db/impact.sql`: the recursive CTE selects `UNION` over a single `id` column, so it finishes even when the data loops. It excludes the starting equipment with `WHERE hit.id <> :equipment_id`. The walk runs over `depends_on_dst`, which EXPLAIN QUERY PLAN shows as `SEARCH d USING COVERING INDEX depends_on_dst (dst_id=?)`. The direction is right: `src` needs `dst`, so a failed `dst` stops `src`.
- `depends_on_dst (dst_id, src_id)`: leads with the column the walks and counts filter on, so the lookups are searches, not scans.
- `equipment.tag UNIQUE`: the `ON CONFLICT (tag)` upsert needs it, and it is present.
- `sync`: the whole file is applied in one `with con:` transaction, so a failure part-way rolls the whole import back.
- `db/dependency_counts.sql`: the group is on `e.id`, the primary key, so the bare `e.tag` and `e.kind` columns are well defined. The count is of rows whose `dst` is the equipment, which is the direction the README describes.

## Not checked
- Nothing was written. plant.db was opened with `mode=ro`, and plans were read with `EXPLAIN QUERY PLAN`. The `sync` fix and migration were not run against a copy, so the cleanup SQL is unexecuted.
- `PRAGMA foreign_keys` being off on a new connection is [run] per the engine notes; the cascade behaviour depends on it.
- If the highest id is decommissioned, SQLite can hand that id to the next insert (no `AUTOINCREMENT` on `equipment`), and the new piece would inherit stale links. This is from the SQLite documentation, not the engine notes, and was not checked. The current maximum id is alive, so it has not happened on this copy.
- No `docs/graph/CONTEXT.md` exists, so the copy is treated as read-only. Whether the planners use `installed_in` outside this repo, and whether ERP tags are permanent, are not in the files.
- The web app's runtime (how often `impact` and `most_depended_on` run, and their latency) is not in the repo, so no rate is stated for the planner views.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

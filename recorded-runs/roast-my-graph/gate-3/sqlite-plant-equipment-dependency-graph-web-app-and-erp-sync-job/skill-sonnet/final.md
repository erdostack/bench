The plant equipment db has one real problem, and it is already in the data. The nightly ERP sync leaves orphan rows behind, so the planners' impact page shows wrong results.

The schema says `ON DELETE CASCADE`, and the sync comment relies on it. But `jobs/sync_from_erp.py` opens its own connection and never runs `PRAGMA foreign_keys = ON`, which is off by default on every new connection. Only `app/db.py` turns it on. So every decommissioned item is deleted from `equipment` and its `depends_on` and `installed_in` rows stay.

On this morning's `plant.db`, `PRAGMA foreign_key_check` returns 1,322 violations, pointing at roughly 260 deleted equipment ids. I opened the copy read-only and compared it with an in-memory copy with the orphans removed:
- **`impact.sql`:** the results differ for 817 of 2,860 pieces of equipment, with 10,527 extra rows in total. The worst case, id 238, returns 193 rows instead of 82. Live equipment is listed as "stops if X fails" only because it depended on something that was scrapped.
- **`dependency_counts.sql`:** it counts dead equipment as dependants. `EQ-00252` shows 13 where 11 are real, and the order of the top 20 changes.

Fix, in this order:
1. After connecting in `sync`, run `PRAGMA foreign_keys = ON`, outside any transaction.
2. Back up, then delete every `depends_on` and `installed_in` row whose ids are not in `equipment`.
3. Run `PRAGMA foreign_key_check` and confirm it returns nothing. The exact statements are in `docs/graph/ROAST.md`.

No query change is needed once the data is clean. A stopgap is to join `equipment` on both ends in the queries. The ROAST also lists the parts that are fine: the indexes, the recursion terminating on loops, and the upsert on `tag`.

Two limits on what I checked. I only had the morning copy, so the production file at `/srv/plant/plant.db` may differ. I also can't tell from the copy whether any equipment id was reused after a delete.

Files written in the repo:
- `docs/graph/ROAST.md`
- `findings.json`

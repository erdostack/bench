I have not changed core. I wrote the backfill as a change file and rehearsed it on `rehearsal`. The donor-systems on-call applies it.

**What the change does**
- `changes/0042_backfill_home_centre_active_donors.py`. It gives each active donor who has given but has no `home_centre` one edge to the centre of their most recent donation, with that donation's day. It adds at most 500 edges per transaction, and a second run does nothing.
- The rule comes from docs/model.md: an active donor who has given has exactly one `home_centre`, the centre of their most recent donation, and a `home_centre` that exists is never changed by a script.

**Two decisions for you**
- Withdrawn donors are not backfilled. Your request said "every donor who has given", but docs/model.md says withdrawn donors have no `home_centre`. That leaves 855 withdrawn donors who have given without one, which is expected under the model.
- 256 of the 4,300 backfilled donors had their most recent donation at DC-09 (Harbour Road), which closed on 2026-06-30. Under the rule they get DC-09 as their usual centre, so the booking app would show a closed centre for them. Migration 0041 says the closed centre's donors were re-homed by donor care by hand, so you may want these 256 excluded or left for donor care. If so, the on-call adds a filter to the `SELECT`.

**Numbers (rehearsal, from a copy of core)**
- target: core, the production donor database. The booking app, donor care and the session planners all use it. Limit: 500 changed rows per transaction (docs/changes.md). Re-runs: safe; the second run returned 0.
- rule: each active donor with at least one donation and no `home_centre` gets one `home_centre` to the centre of their latest donation, with that donation's day · sources: docs/model.md, docs/changes.md, db/schema.sql, changes/0041
- should change: 4,300 edges (independent count on the copy; no donor has two donations on the same day, so each gets exactly one)
- job changed: 4,300 edges, 500 per transaction, 9 transactions
- same rows: yes. The added edges match the expected set on donor, centre and day.
- other rows or tables changed: 0. Nodes are unchanged and no existing edge is changed or removed.
- largest transaction: 500 rows (limit 500, enforced by the `LIMIT`)
- second run: changes nothing (0 rows)
- After the change: active donors who have given and have no `home_centre` are 0, withdrawn donors with a `home_centre` are 0.

**Production: handed back, not run**
- Who runs it: the donor-systems on-call, after PR review: `bin/apply core changes/0042_backfill_home_centre_active_donors.py`
- Check afterwards, which should return 0: `SELECT count(*) FROM nodes d WHERE d.kind='donor' AND d.status='active' AND EXISTS (SELECT 1 FROM edges e WHERE e.kind='donated_at' AND e.src=d.id) AND NOT EXISTS (SELECT 1 FROM edges h WHERE h.kind='home_centre' AND h.src=d.id);`. The `home_centre` count should rise by 4,300.

**Not verified**
- Nothing ran on core. The rehearsal copy was taken from the same data as core (the counts matched).
- The booking app's "your usual centre" screen was not tested.
- The 256 closed-centre donors are a question, not verified against donor care's records.

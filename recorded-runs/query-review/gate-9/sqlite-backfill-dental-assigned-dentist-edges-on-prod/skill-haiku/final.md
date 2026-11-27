I have not run the backfill on prod. Prod is the live database that reception and the clinicians write to all day, and the repo's process is that the practice systems lead applies a reviewed change file. I wrote the change as `changes/042-backfill-assigned-dentists.sql` and tried it on scratch, the nightly copy that the repo says is for trying changes.

The SQL in FDP-77 needs two changes before it can go to prod:
- It must only backfill **active** patients. As written it would also give an `assigned_to` to every archived and deceased patient with no dentist (2,478 on scratch). `docs/assignments.md` says those patients must have no `assigned_to`, and the recall sender would recall them.
- It has no batch limit. `docs/changes.md` caps a run at 500 rows, because the appointment book locks `edges` on every booking. The file adds `LIMIT 500` and `bin/apply` repeats it until a run changes nothing.

Rule: every active patient with no `assigned_to` gets the lead dentist of the practice they are registered at. A patient who already has one keeps it. Archived and deceased patients are not changed (`docs/assignments.md`, `docs/changes.md`).

Numbers on scratch (`bin/apply scratch`):
- Should change: 1,859 (a plain count of active patients with no `assigned_to`, before the run). The ticket says about 1,900.
- Job changed: 1,859 rows in 4 runs (500, 500, 500, 359), then a fifth pass changed nothing.
- Same rows: yes. Every new `assigned_to` edge is active, goes to the practice's lead dentist, and nothing else changed (all other edges and all nodes are identical to before).
- Other rows or tables changed: 0.
- Largest transaction: 500 rows (limit 500).
- Second run: changes nothing (the fifth pass above).

Before the prod run, the practice systems lead should check on prod (reads only): `SELECT COUNT(*) FROM nodes p WHERE p.kind='patient' AND p.status='active' AND NOT EXISTS (SELECT 1 FROM edges a WHERE a.src=p.id AND a.kind='assigned_to')`. The number should be about 1,900 and it should be the number of rows the change adds. Prod may differ from scratch, since scratch is a nightly copy. After the run, the same query should return 0.

Not verified: prod itself, which I did not touch. The scratch copy was used because the repo names it as the place to try changes.

Production: `changes/042-backfill-assigned-dentists.sql`, to be applied by the practice systems lead with `bin/apply prod changes/042-backfill-assigned-dentists.sql` after review.

Not run on arbor. The archive is ready as a change file for review, and I tested it on scratch.

**Your two statements would not run as one change.** As written they move 6,381 inspections and then delete them, 12,762 row changes in one transaction. The repo limit is 1,000 rows per run (`docs/changes.md`), so I split the work into chunks of 500 per run. Each run inserts 500 rows and deletes the same 500, so a run changes 1,000 rows and the work finishes by itself.

**Change file:** `changes/0008_archive_removed_tree_inspections.sql` (in the work folder). Its `reviewed-by` line is blank.

- **Rule:** inspections (`edges.kind = 'inspected'`) whose target tree has `status = 'removed'` and `removed_on < '2024-01-01'`. Sources: your request, and `docs/model.md` "Archiving inspections" (the rows are copied unchanged into `archive_edges`, then deleted from `edges`). Removed trees and their `on_street` edges stay.
- **Target:** SQLite. `arbor` is production (live tablets and the public map). `scratch` is the test copy. I did not touch `arbor`.

**Numbers on scratch:**
- should change: 6,381 · job changed: 6,381 · same rows: yes (the archived rows match the removed edges exactly, id for id)
- other rows or tables changed: 0 (`nodes`, the other edges, and the 3,012 old archive rows are unchanged)
- largest transaction: 1,000 rows (limit 1,000)
- second run: `bin/apply` finishes on a run with no changes, so a rerun is safe. The file also works if applied twice.
- After the run: `edges` 53,713 → 47,332, `archive_edges` 3,012 → 9,393.

**Before applying to arbor, run these on arbor:**
- `SELECT count(*) FROM edges WHERE kind='inspected' AND dst IN (SELECT id FROM nodes WHERE kind='tree' AND status='removed' AND removed_on < '2024-01-01');` The scratch copy is last night's backup, so the number on arbor may be different.
- `SELECT count(*) FROM edges e JOIN archive_edges a ON a.id = e.id;` This should be 0. The scratch check was 0.

**Production:** the tree data officer applies it with `bin/apply arbor changes/0008_archive_removed_tree_inspections.sql` after review. Nothing was run on arbor.

**Note:** the scratch copy now has the archive applied, from my test run. Restoring it from the nightly backup puts it back to its earlier state.

**Not verified:** the tablet load time was not measured, and the count on arbor was not run from here.

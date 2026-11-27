# Roast: gazetteer place merge (SQLite 3.45+)

Verdict: Nothing serious in the SQL itself. The colleague is wrong about the mechanism: a self-loop cannot come out of this merge, and I ran all 140 pairs in order on an in-memory copy with zero self-loops and zero dangling rows. A graph library would not change the real risks, which are data decisions. Do not run the backlog blind: back up `gazetteer.db` first (the merge is not reversible), and settle the 41 pairs that disagree on `kind` before running those.

Judged against:
- Engine: SQLite, from `sql/schema.sql` and `README.md` (3.45+ stated; checked on 3.53.1).
- Size: 1,500 places, 3,466 borders, 168 aliases (counted in `gazetteer.db`). Backlog: 140 pairs, 140 distinct dup ids, all present.
- Undirected border, each pair stored once with the smaller id first, length in km (`README.md`, CHECK `a < b` in `sql/schema.sql`).
- Merge meaning: the copies are "the same place" and "usually border each other" (`README.md`).
- The app reads `border` for "neighbours", sorted by km (`sql/queries.sql`, `README.md`).
- Operations: `tools/merge.py KEEP DUP` runs `sql/merge_place.sql` in one transaction (`tools/merge.py`).

## Findings

### medium: `place.kind`
41 of the 140 pairs disagree on kind, and the merge keeps only the keep's kind.
Problem: The pairs share a name, and their kinds differ: for example 267 (parish) and 1209 (town), 726 (town) and 1220 (parish). Step 5 of `sql/merge_place.sql` (`DELETE FROM place WHERE id = :dup`) removes the dup's kind with no check or record. README says the copies are "the same place", but 41 of 140 pairs contradict that on kind, and 102 neighbour collisions sit inside those pairs. The files do not say which kind is right, or whether these are two real places with one name. This is a question the data cannot answer, so it is medium here; if these are distinct places, the merge is wrong and it becomes high.
Fix: Before running, list the 41 pairs and decide per pair (merge, or keep both and drop them from the backlog). If a merge is kept, record the dup kind in the merge log (see the finding below) before deleting.

### medium: `border.km`
Step 2 of `sql/merge_place.sql` drops dup's boundary length for every shared neighbour.
Problem: `INSERT OR IGNORE INTO border` keeps keep's km when both places border the same neighbour. In the backlog, 349 such pairs of rows exist (checked on an in-memory copy, after each merge in order), and in all 349 the two lengths differ (for example 842/1201 with 811: 4.24 km versus 6.37 km). Those values are discarded and cannot be recovered afterwards. `neighbours` sorts by km, so the ranking changes silently. The SQL comment states the rule ("keep's own length wins"), so the choice is documented; the problem is that the discarded values are real measurements and their disagreement says the two outlines do not describe one boundary.
Fix: Keep both measurements in a log before the merge, and decide the stored km deliberately (for example the longer, or the mean, or a re-measured value from the geometry). If the km is only for ordering, state that in `README.md`.

### medium: `sql/merge_place.sql`
Problem: Nothing records what a merge removed. Step 5 deletes the dup row, step 3 deletes its borders, and step 4 deletes its aliases. Once run, the dup id, its 110 border rows, the 349 dropped km values and its kind are gone, and the backlog contains pairs whose correctness is open (see the kind finding). No restore path exists in the files.
Fix: Write a `merge_log(keep, dup, kind, border rows removed, km dropped, merged_at)` row in the same transaction, or copy `gazetteer.db` before the run. The backup is the minimum; the log makes the merge auditable.

### low: `alias`
Problem: Step 4 writes the dup's own name as an alias of the keep. In all 140 pairs the names are identical, so 131 alias rows (168 to 299) repeat `place.name` and add nothing to `lookup`.
Fix: Insert the dup's name as an alias only when it differs from the keep's name: add `AND name <> (SELECT name FROM place WHERE id = :keep)` to the second statement.

### low: `merge` (tools/merge.py)
Problem: `merge` does not check that either id exists. A nonexistent dup makes every statement a no-op and returns normally; a mistyped id looks like a successful merge.
Fix: Check both ids exist, and raise `ValueError` if one does not, before the transaction starts.

### low: `statements` (tools/merge.py)
Problem: The splitter removes only lines that start with `--` and then splits on `;`. A comment after code on the same line that contains a `;` would split a statement in two. Nothing in the current file triggers it.
Fix: Keep the SQL in separate files per statement, or split with `sqlite3.complete_statement` on a running buffer.

## Holds up
- `border` CHECK `(a < b)` with `min`/`max` in step 2: undirected pairs stay canonical. Checked: 0 rows with `a >= b` after 140 merges.
- Step 1 (`DELETE FROM border WHERE (a = :keep AND b = :dup) OR (a = :dup AND b = :keep)`) runs before step 2: the edge between the two copies is removed before it can become a self-loop. Checked: 0 self-loops after 140 merges.
- Step order with foreign keys on (`tools/db.py` sets `PRAGMA foreign_keys = ON`): borders and aliases of dup are removed before `place` is deleted, so step 5 cannot leave dangling references. Checked: 0 dangling border or alias rows.
- One transaction (`with con:` in `tools/merge.py`): any error rolls back the whole merge. A missing keep fails at the foreign key in step 2.
- `border_b (b, a)` alongside the primary key `(a, b)`: serves both directions in `neighbours` (`sql/queries.sql`).
- The backlog has no chains: none of the 140 dup ids is a keep elsewhere, and each dup appears once. Keeps 8, 107, 304, 679, 734, 824, 932 and 1009 repeat, which is fine because each merge is independent.
- Names: every dup name reaches the keep as an alias, so `lookup` finds the keep under the dup's name.

## Not checked
- Whether the 41 kind mismatches are duplicates or distinct places: the files do not say, and nothing outside them was checked.
- The app's use of dup ids (stored references, bookmarks): not in these files, so a dangling id would not show here.
- The copies' geometry (which outline is right): not in the repo.
- Nothing was written: `gazetteer.db` was opened read-only and the simulation ran on an in-memory copy.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

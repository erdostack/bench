# Roast: gazetteer place merge (sql/merge_place.sql, tools/merge.py)

Verdict: No, your colleague is not right: this merge does not produce self-loops or lose edges, and it does not need rewriting on a graph library. I ran the whole 140-pair backlog on an in-memory copy of `gazetteer.db`: 3,007 borders came out, exactly the set you get by contracting each dup into its keep and dropping loops (0 missing, 0 extra), no self-loops, no foreign-key violations. Nothing serious: two `low` notes, and the 41 pairs whose kinds differ are worth a look before you run it for real.

Judged against:
- Engine: SQLite 3.45+, opened by `tools/db.py` with `PRAGMA foreign_keys = ON` (README.md, tools/db.py); the sample was inspected on SQLite 3.53.1.
- Data: `gazetteer.db` holds 1,500 places, 3,466 borders, 168 aliases. Production size: not stated.
- Border: undirected, each pair stored once with the smaller id first (`CHECK (a < b)`), `km` is the shared boundary length; the app's neighbours and walk features read it (README.md, sql/schema.sql).
- Merge: the 2019 import created places twice and the two copies usually border each other; `tools/merge.py KEEP DUP` folds one into the other through `sql/merge_place.sql`, in one transaction per pair; 140 pairs in `backlog.csv` (README.md, sql/merge_place.sql).
- Read rate: not stated; the merge is a one-off backlog.

## Findings

### low: `kind`
A merge that keeps a town and quietly forgets the same place was filed as a parish.
Problem: Question to confirm: the merge keeps the keep row's `kind` and drops the dup's without a trace. In `backlog.csv`, 41 of the 140 pairs have different kinds (for example 267 is a parish and 1209 a town; 726 is a town and 1220 a parish). The files do not say which kind is right for a merged place, or whether a differing kind means the pair is not a duplicate.
Fix: Before running, list the 41 pairs (compare `kind` of keep and dup for every row of `backlog.csv`), decide for each which kind is correct, swap keep and dup where the dup's kind is the one to keep, and drop pairs that are not duplicates. If you want a differing kind recorded, add a step to `sql/merge_place.sql` before the final `DELETE FROM place` that sets it explicitly.

### low: `merge_place.sql`
Problem: Step 4 (`INSERT OR IGNORE INTO alias (place_id, name) SELECT :keep, name FROM place WHERE id = :dup`) adds the dup's name as an alias of keep even when it equals keep's own name. All 140 dups in the backlog have the same name as their keep, so the full run adds about 131 alias rows that repeat `place.name` (168 to 299 in the copy). The `lookup` query uses `UNION`, so users see no duplicates; the rows are clutter.
Fix: Only add it when it differs: `INSERT OR IGNORE INTO alias (place_id, name) SELECT :keep, name FROM place WHERE id = :dup AND name <> (SELECT name FROM place WHERE id = :keep);`.

## Holds up
- Step 1 of `merge_place.sql` (delete the keep-dup border): the only way this merge could create a self-loop is a border between the two copies becoming a border from keep to keep. Step 1 deletes it before anything moves, and `CHECK (a < b)` would reject a loop anyway. 110 of the 140 pairs border each other; for the other 30 the delete does nothing, which is also correct.
- Step 2 (`INSERT OR IGNORE ... min(:keep, other), max(:keep, other)`): `min`/`max` keep the smaller-id-first rule, so the move cannot violate the CHECK. `INSERT OR IGNORE` means a neighbour that keep already has keeps keep's length, as the comment says (349 shared neighbours in the backlog, all with differing lengths, keep wins by design). No edge is lost: the dup's other neighbours are all re-pointed, and the final border set matches an independent contraction of the graph. No two dups of one keep disagree about a neighbour they alone share, so the order of the backlog does not change the result on this data.
- Steps 3 to 5 (delete dup's borders, move aliases, delete the place): ordered children first, so the foreign keys never fail. `alias` and `border` are the only tables that reference `place`.
- `tools/merge.py` `merge`: `with con:` makes each pair atomic; `statements()` splits on `;` and drops comment lines, which works because no statement or comment contains a `;` (7 statements are produced). A typo in KEEP is caught: the alias insert would point at a missing place and the foreign key aborts the pair, leaving the dup in place (tested on the copy). A pair run twice is a no-op the second time (also tested). No keep appears as a dup in the backlog and no dup repeats, so merges do not chain.
- A graph library: the job is contracting 140 vertices in a 3,466-edge graph with a stated rule for conflicting lengths, plus moving aliases and deleting rows. The library would still need the same decisions (drop the keep-dup edge, keep's length wins) and the result would then have to be written back to SQLite. The SQL already does this correctly.
- `border_b` and the primary key `(a, b)`: both directions of the `neighbours` query are index searches; the merge reads by `a = :dup` and `b = :dup`, which these serve.

## Not checked
- Speed and behaviour at production size: not stated, and nothing was timed.
- `lookup` filters `place.name` and `alias.name` and no index leads with either (`alias` is keyed by `(place_id, name)`). At the sample's 1,500 places this is not a cost; whether it matters in production depends on a size the files do not give.
- The "walk from A to B" feature: its code is not in the repo.
- Whether the 140 pairs are truly duplicates: that is the data owner's call. The real `gazetteer.db` was opened read-only; the merge was run only on an in-memory copy. Take a file copy of `gazetteer.db` before the real run.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

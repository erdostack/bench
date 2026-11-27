**Your colleague is wrong, so you do not need a graph library. The merge logic is sound. Check one data problem in the backlog before you run it.**

The statements handle both worries:

- **Self-loops.** Step 1 deletes the `keep`-`dup` border first, which is the one case where remapping would give a self-loop. Step 2 then remaps with `min(:keep, other)` and `max(:keep, other)`, which preserves the `a < b` rule.
- **Lost edges.** Step 2 copies every other border of `dup` onto `keep` before step 3 deletes the originals. The only edges that disappear are the `keep`-`dup` border and borders `keep` already has, where its length wins, as the README and SQL comment say. Everything runs in one transaction with foreign keys on, and `dup` is deleted last.

To check this, I ran all 140 pairs in order on a copy of `gazetteer.db` and compared the result with the expected edge set. I built that set by relabelling each `dup` as its `keep`, dropping self-loops and letting `keep`'s length win. The two matched exactly, with 3,466 borders before and 3,007 after. The result had no self-loops, no `a >= b` rows and no foreign-key violations. The backlog has no chains: no id is a `dup` twice, or both a `dup` and a `keep`. Your real `gazetteer.db` is untouched.

**What to do first (7 items in `findings.json`):**

- **Medium, check the backlog.** 41 of the 140 pairs have different `kind` values, for example a parish and a town with the same name. The merge keeps only `keep`'s kind. Confirm those 41 really are the same place, or you will destroy a real place.
- **Medium, no record of the merges.** After the merge there is no old-to-new id mapping, no dry-run and no batch mode. Back up `gazetteer.db` and loop over the CSV yourself.
- **Low.**
  - A missing or already-merged `dup` succeeds silently.
  - `INSERT OR IGNORE` is broader than needed.
  - The dup's name is added as a redundant alias, about 131 rows.
  - The SQL is split on `;` naively.
  - The default DB path is relative to the current directory.
  - `place.name` and `alias.name` are not indexed.

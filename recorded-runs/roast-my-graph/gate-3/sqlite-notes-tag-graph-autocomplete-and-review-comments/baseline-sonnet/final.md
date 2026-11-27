Short version: the reviewer is wrong about the autocomplete. The schema has a few real problems he didn't mention.

**Autocomplete (comment 1): not a problem, no FTS5 needed**
- `tag.name` is declared `COLLATE NOCASE UNIQUE`, so its automatic index (`sqlite_autoindex_tag_1`) is case-insensitive. SQLite can turn a `LIKE 'abc%'` into a range search on that index when the column uses NOCASE.
- `EXPLAIN QUERY PLAN` on `SUGGEST` against `tags.db` (80,000 tags) shows `SEARCH tag USING COVERING INDEX sqlite_autoindex_tag_1 (name>? AND name<?)`. There is no scan and no temp b-tree, because the index order already gives `ORDER BY name`.
- Six `suggest()` calls took about 0.3 ms in total. `LIKE '%ab%'` on the same table takes about 22 ms, which is the scan he was worried about, but `suggest()` never builds a leading-wildcard pattern.
- The regex rejects `%` and `_` before they reach `LIKE`, so there is no wildcard injection.
- Two things would break this: running `PRAGMA case_sensitive_like = ON`, or adding infix search later. An FTS5 table would add write and storage cost for nothing today.

**Ancestors query (comment 2): it cannot loop**
- `UNION` (not `UNION ALL`) drops ids already in the walk, so the recursion stops by itself. I ran it on the cycle that is in the sample: tags 11, 12 and 13 form a loop, and the query returned normally for each of them.
- That cycle is the real finding. The schema only has `CHECK (child_id <> parent_id)`, so longer cycles are allowed and one already exists in the data. Any code that walks the tree without `UNION` could loop on it.

**Comment 3, `note.updated` as TEXT:** this is fine in SQLite, and every value in the sample is an ISO date. The weak spot is that the values are dates only, so the `ORDER BY` has ties, and nothing checks the format.

**Other findings**
- `tag_note` uses `INSERT OR IGNORE INTO note_tag`, and OR IGNORE does not cover foreign key violations. Nothing in `app/` turns on `PRAGMA foreign_keys`, and `tags.db` has it off on a new connection. A bad `note_id` therefore inserts an orphan row, and the `ON DELETE CASCADE` clauses do nothing. The sample has no orphans right now.
- `notes_with_tag.sql` sorts every note of a tag with a temp b-tree before taking 50. With 12 notes at most per tag in the sample you can't see it. With 9 million note_tag rows it depends on how large the popular tags are, which I couldn't measure.

`findings.json` in the repo root has five entries (one per problem above, including the two reviewer comments I checked) in the format you asked for. I only read from `tags.db` and did not change it.

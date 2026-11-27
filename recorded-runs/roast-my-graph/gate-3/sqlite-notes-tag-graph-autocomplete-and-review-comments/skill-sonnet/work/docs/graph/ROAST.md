# Roast: notes tag graph (db/, app/)

Verdict: Nothing serious, and on the autocomplete the reviewer is wrong: `suggest()` does not scan the tag table. SQLite searches `sqlite_autoindex_tag_1` for the prefix, so no FTS5 or trigram table is needed. The loop question is answered by the query itself and it is safe as written. One low question is left.

Judged against:
- Engine: SQLite 3.45 via Python's sqlite3 (README.md). The sample was run on SQLite 3.53.1, not 3.45.
- Size: about 80 thousand distinct tags, 9 million note-tag rows; the tag box autocompletes on every keystroke (README.md). The sample has 80,000 tags, 50,000 notes, 199,993 note_tag rows and 30,003 tag_parent rows.
- Writers and the connection setup: not stated (the connection is passed in from outside the repo).

## Findings

### low: `note_tag`
The cascade is a promise that the connection has to keep, and nobody in the repo is on record keeping it.
Problem: `note_tag` and `tag_parent` declare `ON DELETE CASCADE` and `REFERENCES`, but SQLite ignores foreign keys unless each connection runs `PRAGMA foreign_keys = ON`, and nothing in the files does (a new connection reports it off). `tag_note()` inserts `note_id` unchecked. The sample passes `PRAGMA foreign_key_check` with no orphans, and no delete statement exists in the files, so this is a question: does the code that opens the connection switch foreign keys on?
Fix: confirm where the connection is created; run `PRAGMA foreign_keys = ON` right after every `sqlite3.connect(...)` there, or in a small helper used by all callers. If foreign keys are already enabled elsewhere, no change.

## Holds up
- `suggest` in app/autocomplete.py (`LIKE ?` on `tag.name`): the reviewer's premise that LIKE cannot use an index in SQLite is not true when the column and index use NOCASE, which is the default LIKE comparison. `tag.name` is declared `COLLATE NOCASE UNIQUE`, so its automatic index `sqlite_autoindex_tag_1` has that collation. `EXPLAIN QUERY PLAN` on the exact SUGGEST statement with a bound `'ab%'` gives `SEARCH tag USING COVERING INDEX sqlite_autoindex_tag_1 (name>? AND name<?)`, and the same for `'AB%'`. `ORDER BY name LIMIT 10` reads in index order, so it stops after ten rows. The bound pattern is safe because the regex in `suggest` only allows letters, digits and hyphens, so no `%` or `_` reaches the pattern. What would change that: a `PRAGMA case_sensitive_like=ON` on the connection, a different collation on `tag.name`, or an SQLite older than the one tested (the plan was checked on 3.53.1, not 3.45).
- `tag_ancestors.sql`: `UNION` over a recursive step that carries only `id` drops repeated ids, so a loop in `tag_parent` ends the walk. I ran it on a three-tag loop (1, 2, 3, back to 1) and it returned tags 2 and 3 and stopped. On the sample, the deepest ancestor set over 3,000 tags is 22 tags. The walk uses `tag_parent` primary key `(child_id, parent_id)`, so each step is an index search. A depth limit is optional insurance, not a defect.
- `tag_parent` with `tag_parent_by_parent`: `tag_children.sql` searches `tag_parent_by_parent (parent_id=?)`, and `tag_ancestors.sql` the primary key by `child_id`. Both directions are covered.
- `notes_with_tag.sql`: searches `note_tag_by_tag (tag_id=?)` and sorts the tag's notes for `ORDER BY n.updated DESC LIMIT 50`. The busiest tag in the sample has 12 notes, so the temp sort is tiny. What would change that: tags with many thousands of notes on a hot path.
- `note.updated` TEXT (review comment 3): the sample holds ISO dates (`2026-07-17`) with no exceptions, which sort correctly as text. Not a finding.
- `tag.name` CHECK and `NAME` in app/tagging.py agree with `PREFIX` in app/autocomplete.py; `INSERT OR IGNORE` plus select in one transaction is a correct get-or-create.

## Not checked
- SQLite 3.45 itself: everything was run on 3.53.1 through Python's sqlite3, read-only for `tags.db` (the loop test used an in-memory database).
- Speed at 9 million note-tag rows; the sample is smaller than the README's size, so only the plans were judged.
- Where the application opens its connection.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

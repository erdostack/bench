# Roast: tag graph (db/ and app/)

Verdict: Sam is wrong about the autocomplete. The LIKE in app/autocomplete.py uses the unique index on tag.name, because that column is COLLATE NOCASE and SQLite can range-scan a case-insensitive prefix. Nothing serious; the real costs are a sort on every tag page and foreign keys that are declared but never switched on.

Judged against:
- SQLite 3.45 via Python sqlite3 (README.md). The sample reports SQLite 3.53.1.
- About 80 thousand distinct tags and 9 million note-tag rows across the hosted workspaces; the tag box autocompletes on every keystroke (README.md).
- Tag names are letters, digits and hyphens, 1 to 40 characters (db/schema.sql CHECK; app/tagging.py NAME).
- A tag can have several parents; a note has any number of tags (README.md).
- Sample tags.db: 80,000 tag, 50,000 note, 199,993 note_tag, 30,003 tag_parent rows.

## Findings

### medium: `note_tag`
The rant: the schema promises that deleting a note cleans up after itself, and the application has never heard of that promise. SQLite does not enforce foreign keys unless someone asks it to, and nobody has.
Problem: note_tag declares REFERENCES note and tag with ON DELETE CASCADE, but no file in the repo runs PRAGMA foreign_keys = ON. The sample connection reports 0. tag_note in app/tagging.py accepts any note_id, so a note_tag row for a missing note is stored without error. Trigger: a note deletion, or a tag_note call with an id that is not in note. The trigger is not in these files.
Fix: Run PRAGMA foreign_keys = ON on every connection the application opens, where that connection is created (not in these files). Then confirm that SELECT count(*) FROM note_tag WHERE note_id NOT IN (SELECT id FROM note) stays 0.

### medium: `notes_with_tag`
The rant: the query finds the 50 newest notes for a tag by reading every note with that tag, sorting the lot, and then throwing most of it away. The sample is kind enough to have 12 notes for its busiest tag.
Problem: the query filters on note_tag_by_tag (tag_id, note_id), then ORDER BY n.updated DESC LIMIT 50. EXPLAIN QUERY PLAN on tags.db shows USE TEMP B-TREE FOR ORDER BY. The README's 9 million rows across 80 thousand tags means popular tags will have far more notes than the sample, and the sort runs on each tag page.
Fix: Carry updated onto note_tag (copied from note), index (tag_id, updated DESC, note_id), and read that index in order with LIMIT 50. The copy must be kept in step by whatever writes note.updated, which is not in these files. A stopgap, labelled as one: an index on note (updated) with the query walking note in that order, which only helps tags with few notes.

### low: `note`
The rant: a timestamp stored as text, sorted as text, and a tie-breaker that does not exist. The data is tidy for now, which is how these things start.
Problem: note.updated is TEXT with no format check, and notes_with_tag.sql orders by it without a tie-breaker. All 50,000 sample values are 10-character YYYY-MM-DD and sort correctly, so Sam's nit depends on whether another format can reach the column, which the files do not say. Because the values are dates without times, many notes share one, so the 50 shown can change between runs.
Fix: Add CHECK (updated GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]') if the dates are always ISO, or store an INTEGER timestamp. Add n.id DESC as a second sort key in notes_with_tag.sql.

### low: `tag_parent`
The rant: the schema bans a tag from being its own parent, and then allows a family tree in which everyone is their own great-grandparent.
Problem: CHECK (child_id <> parent_id) blocks only self-parents. Cycles of three or more are allowed by the schema, and no file forbids them. tag_ancestors.sql still terminates, because UNION drops rows already seen. The sample has no two-cycles; longer cycles were not checked.
Fix: If the hierarchy must be a DAG, reject an edge whose parent is already a descendant of its child, in whatever code inserts tag_parent rows. If cycles are allowed, document that next to tag_ancestors.sql.

## Holds up
- `tag` autocomplete (app/autocomplete.py, SUGGEST): the query is `name LIKE ? ORDER BY name LIMIT 10`. EXPLAIN QUERY PLAN with a bound parameter shows SEARCH tag USING COVERING INDEX sqlite_autoindex_tag_1 (name>? AND name<?) with no temp sort. The UNIQUE constraint on a NOCASE column builds that index. Timings on the sample were 0.01 to 0.3 ms. This holds only while tag.name keeps COLLATE NOCASE and case_sensitive_like stays off. Changing either makes the LIKE unindexable, and that would be the time to act on Sam's concern.
- `tag_ancestors.sql`: the recursion uses UNION, so a row already in up is dropped and the walk ends even on a cycle. Sample has no two-cycles. This holds only while the query stays UNION; UNION ALL would loop forever on a cycle.
- `tag_children.sql`: served by tag_parent_by_parent (parent_id, child_id); the plan uses it.
- Input check in app/autocomplete.py: the prefix is limited to letters, digits and hyphens, so no LIKE wildcard reaches the query.

## Not checked
- The sample is small (50,000 notes, 200,000 note-tag rows). Timings describe plan shape, not behaviour at 9 million rows.
- Whether any application code outside these files sets PRAGMA foreign_keys or deletes notes.
- Cycles of three or more in tag_parent: not checked in the sample.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

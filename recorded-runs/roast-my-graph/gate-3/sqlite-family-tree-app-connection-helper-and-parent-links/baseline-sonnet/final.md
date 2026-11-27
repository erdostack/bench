Your friend is wrong on the main point, in this repo as it stands.

It is true that SQLite does not enforce foreign keys unless you turn them on for each connection. But `app/db.py` does that: `connect()` runs `PRAGMA foreign_keys = ON` before returning, and `delete_person` and the importer both go through it, so the `ON DELETE CASCADE` in `db/schema.sql` works. I checked three ways:

- `tests/test_people.py` already covers it: `test_delete_cascades` deletes a person and asserts their `parent_of` rows are gone, and `test_link_to_missing_person_is_rejected` asserts the missing-parent insert fails. Both pass (2 passed).
- `PRAGMA foreign_key_check` on a copy of `family.db` returns no violations across 6,000 people and 11,920 `parent_of` rows. There are no dangling parent links, even though you have presumably deleted people before.
- He does not need a cleanup job or hand-written triggers.

His point would be right in one case. The Flask front end is not in this repo, and if it opens its own `sqlite3.connect()` without the PRAGMA, deletes from there would leave dangling rows. The same goes for editing the file in a DB browser or the `sqlite3` CLI. I put this in the findings as a low item against `app/people.py`. Make the front end use `app.db.connect()`.

The real problems are elsewhere, mostly in `tools/import_gedcom.py`:

- **Dates are dropped:** the importer never reads BIRT or DEAT. In `family.db` 5,960 of 6,000 people have no birth date and nobody has a death date. That is the most useful thing to fix, because dates are what help you merge two people with the same name.
- **No provenance:** nothing stores which file or GEDCOM id a person came from. Importing a file twice doubles everyone, and merging people across relatives' files by hand has nothing to anchor on. The 6,000 people have only 96 distinct names, and 64 same-named pairs share a child as its two parents.
- **Parser bugs:** non-INDI/FAM records (NOTE, SOUR and similar) leave the previous person active, so their NAME lines can overwrite that person's name. `John /Smith/ Jr` becomes the surname `Smith/ Jr`, and a NAME with no slashes gets an empty surname.
- **Relationship type lost:** every parent link comes in as `birth`, and all 11,920 rows are `birth`.

The rest is minor: no cycle guard on `parent_of`, no date format check, the ancestor queries have no generation or ordering, and the tests only run from the repo root and do not cover the queries or the importer.

All nine findings are in `findings.json` in the repo root, with element, severity, problem and fix. I did not modify any source files, and I only read a throwaway copy of `family.db`, which I deleted.

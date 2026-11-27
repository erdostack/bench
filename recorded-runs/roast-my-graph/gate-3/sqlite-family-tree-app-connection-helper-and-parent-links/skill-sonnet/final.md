Your friend is wrong. SQLite does leave foreign keys off by default. But `connect()` in `app/db.py` runs `PRAGMA foreign_keys = ON`. It's the only place the app opens the database, and `tools/import_gedcom.py` uses it too, so the `ON DELETE CASCADE` in `schema.sql` is enforced.

I checked this on a copy of `family.db`, so your real file is untouched. Deleting the person with the most links removed all 10 of their `parent_of` rows, and `PRAGMA foreign_key_check` stayed empty. Your current `family.db` has no dangling links either, across 6,000 people and 11,920 links. The two tests in `tests/test_people.py` pass, and they check both the cascade and the rejection of a link to a missing person. You don't need a cleanup job or cascade triggers.

I found no problems in `app/`, `db/` or `tools/`, so `findings.json` is an empty list, `[]`. The write-up in `docs/graph/ROAST.md` says why each part holds up.

Two things you might not expect:
- **Re-importing:** running the same GEDCOM file twice would add every person again. Your README says each file is imported once, so I didn't count it as a bug.
- **`kind`:** the importer doesn't read adoptive or step relationships, so every imported link gets `kind = 'birth'`. That would be a new feature, not a bug.

Your friend's point would become true if some other code opened `family.db` without going through `connect()`. The pragma is per connection, so keep every connection going through that function.

I couldn't check the Flask front end or the UI merge, because they're not in the repo, or any real GEDCOM files, so I read the parser but didn't run it.

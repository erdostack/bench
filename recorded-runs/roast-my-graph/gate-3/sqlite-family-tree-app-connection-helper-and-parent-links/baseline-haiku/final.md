Your friend is wrong about the app, and the data proves it.

SQLite does ignore foreign keys by default, but `app/db.py` turns them on in `connect()` for every connection. `delete_person` goes through that, and `tests/test_people.py` has a test that a delete cascades. In `family.db` there are 11,920 parent links and zero rows pointing at a missing person, zero self-links, and no cycles. So nothing piles up. The one place his point could bite is a raw `sqlite3.connect` somewhere outside this repo, such as the Flask front end you mentioned. Anything that opens the file without `connect()` runs with foreign keys off.

The bugs that matter are in the GEDCOM importer:
- A `NAME` line under a `SUBM` or `REPO` record overwrites the last person's name. In a sample file, Ann /Jones/ came in as "Jane Submitter" with no surname. This is the one to fix first, since it changes names in your real tree.
- The importer never reads birth or death dates, so imported people have no dates.
- Running the import twice on the same file creates every person twice, because nothing records where a person came from.

None of this was caught because nothing tests the importer. The full list, with elements, severities and fixes, is in `findings.json` in the repo root.

I checked `family.db` read-only, on an in-memory copy, and did not change it.

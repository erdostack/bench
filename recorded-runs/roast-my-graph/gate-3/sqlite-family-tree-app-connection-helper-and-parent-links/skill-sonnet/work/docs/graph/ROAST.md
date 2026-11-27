# Roast: kin (app/, db/, tools/, against family.db)

Verdict: Sound, and no, your friend is not right. SQLite does leave foreign keys off by default, but `app/db.py` runs `PRAGMA foreign_keys = ON` in `connect()`, which is the one place the app opens the database, so the `ON DELETE CASCADE` in db/schema.sql is enforced. I ran it on a copy of `family.db`: deleting the person with the most links removed all 10 of their `parent_of` rows, and `PRAGMA foreign_key_check` stayed empty. `family.db` as it is now has no dangling links either (11,920 rows, `foreign_key_check` returns nothing). Nothing needs to change. No cleanup job and no cascade triggers: they would duplicate what the engine already does.

Judged against:
- Engine: SQLite; this machine's Python `sqlite3` is 3.53.1 (run). Version of the user's deployment: not stated.
- Size: about 6,000 people (README.md); `family.db` has 6,000 people and 11,920 `parent_of` rows, no cycles, no person with more than two parents.
- Writers: the Flask front end (not in this repo) through `app/`, and `tools/import_gedcom.py`, run once per GEDCOM file; duplicate people across relatives' files are merged by hand in the UI afterwards (README.md).
- Reads that matter: `ancestors` and `descendants`. How often they run: not stated.
- Stated guarantee: deleting a person removes their parent and child links (`delete_person` docstring, db/schema.sql).

## Findings

None.

A reviewer who finds nothing wrong in a schema that cascades on both sides, checks `kind`, forbids a person being their own parent, has an index for each direction and turns the pragma on in the one place connections are made is looking at the rarest thing in this business: a family tree that remembers who its relatives are. It is almost suspicious.

## Holds up
- `PRAGMA foreign_keys = ON` in `connect` (app/db.py): the answer to the review in docs/friend_review.md. The claim that `ON DELETE CASCADE` is "just decoration" does not hold, because every connection comes through this function (checked every file; `tools/import_gedcom.py` and `app/people.py` both call `connect()`), and the pragma is set before any statement runs. tests/test_people.py asserts the cascade (`test_delete_cascades`) and the rejection of a link to a missing person (`test_link_to_missing_person_is_rejected`), and both pass here. Would change if: a second way of opening `family.db` appears (for example the Flask app calling `sqlite3.connect` directly); the pragma is per connection.
- `parent_of`: a node-like table between two people? No: it is the relationship itself, with one row per link, both endpoint keys, a `kind` with a `CHECK`, and `PRIMARY KEY (parent_id, child_id)` stopping duplicates. Nothing else refers to it. Right as it is.
- `parent_of_child` and the primary key: the primary key `(parent_id, child_id)` serves `descendants` (lookups by `parent_id`), and `parent_of_child (child_id, parent_id)` serves `ancestors` (lookups by `child_id`). Each direction has its index. At 6,000 people the recursive queries returned sets of up to 5,450 people in about 2.4 ms per query on average over 600 queries here.
- `ancestors.sql` and `descendants.sql`: recursive with `UNION` over the id alone, so a loop in the data could not make them run forever, and `family.db` has no loop anyway (a `CHECK (parent_id <> child_id)` rules out only a person being their own parent; longer loops are possible in principle and not present). Safe as written. A parent-of cycle check on insert would be optional insurance, not a defect.
- `delete_person`: one statement in a transaction; the cascade does the rest.
- `import_gedcom.load`: `INSERT OR IGNORE` into `parent_of` makes a family with the same couple and child twice harmless; it writes everything in one transaction, so a failed import rolls back. Re-running the same file would insert every person again (nothing in `person` is unique), but the README says each file is imported once and duplicates are merged by hand, so that is the stated workflow and not a defect. A guard against re-import is optional insurance.
- Everything imported gets `kind = 'birth'` (the column default): GEDCOM adoptive and step relationships (`PEDI` tags) are not read. Nothing in the files says they should be, and the data has only `birth` rows; if you want those recorded, that is a new feature, not a bug.

## Not checked
- The Flask front end and the in-UI merge of duplicate people are not in this repo, so I could not check how merged people's `parent_of` rows are rewritten (the primary key and `CHECK` would reject a merge that makes someone their own parent).
- Real GEDCOM files: none are in the repo, so the parser was read, not run.
- Names in `family.db` are swapped out, so I judged structure only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

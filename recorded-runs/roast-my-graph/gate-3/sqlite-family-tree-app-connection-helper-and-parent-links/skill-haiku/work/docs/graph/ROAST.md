# Roast: kin (app/, db/, tools/)

Verdict: Nothing serious. The friend is half right. SQLite does leave foreign keys off on a new connection, and a plain connection does leave dangling `parent_of` rows after a delete. But app/db.py turns the pragma on for every connection the app opens, `family.db` has no dangling rows, and a delete through `delete_person` removes the links. No cleanup job or triggers are needed. The only thing to watch is code that opens its own connection outside `app/db.connect()`.

Judged against:
- Engine: SQLite 3.53.1 (run here). The repo does not state a version.
- Size: about 6,000 people (README.md). family.db has 6,000 person rows and 11,920 parent_of rows (counted from the file).
- Writers: GEDCOM imports, once per file, and the Flask front end, which is not in this repo (README.md). Frequency: not stated.
- Interactive paths: ancestor and descendant queries (db/ancestors.sql, db/descendants.sql) and delete_person. Frequency: not stated.
- Stated guarantee: a person's parent and child links go with them (`ON DELETE CASCADE`, db/schema.sql, the docstring of delete_person).
- Stated rule: each relative's file is imported once; duplicates are merged by hand in the UI (README.md).
- family.db is the real tree with names swapped out (task note). Its schema matches db/schema.sql.

## Findings

### medium: `parse`
A submitter or repository record in a GEDCOM file renames the last person in the file.
Problem: `parse` only resets `cur` on INDI and FAM records. A later level-0 record of another type (SUBM, REPO) leaves `cur` on the last person, and its `1 NAME` line then overwrites that person's name. Tested on a small file: a trailing `0 @U1@ SUBM` with `1 NAME Jane Submitter` turned the last INDI, "Bob Lee", into "Jane Submitter". The shipped data has no GEDCOM file, so this needs a file whose SUBM or REPO record comes after the last INDI. It is rated medium for that reason.
Fix: Set `cur = None` on every level-0 record that is not INDI or FAM. Read `NAME` only when `cur` is an INDI. Add a parse test with a trailing SUBM record.

### low: `delete_person`
Problem: The cascade depends only on the pragma set in app/db.connect. The delete does not remove `parent_of` rows itself. A test in memory showed that the same delete through a plain sqlite3 connection left 4 rows referring to the deleted person. Nothing in this repo opens such a connection, but the Flask front end is not here.
Fix: In `delete_person`, delete the person's `parent_of` rows in the same transaction (`DELETE FROM parent_of WHERE parent_id = ? OR child_id = ?`). Keep the declared constraint, so the write path no longer depends on the connection setting.

### low: `load`
Problem: The import runs `INSERT OR IGNORE` on parent_of, so a GEDCOM self-link (for example a person listed as their own child) is dropped without a message. The check `parent in ids and child in ids` drops links to unknown records just as silently. Each run also inserts every person again, so importing the same file twice doubles the tree, and the README's "once per file" rule is not checked by the code.
Fix: Count and report skipped links. Use a plain INSERT for parent_of and report the IntegrityError. Refuse to import a file whose name or content hash is already recorded (a small import table), or check for existing rows before inserting.

## Holds up
- `db/schema.sql`: both foreign keys declare `ON DELETE CASCADE`, the `CHECK (parent_id <> child_id)` rejects self-links at the table, and `WITHOUT ROWID` with the (parent_id, child_id) key suits the table. `parent_of_child (child_id, parent_id)` serves the ancestors join, which the plan confirms (SEARCH ... COVERING INDEX parent_of_child). Descendants search the primary key on parent_id (SEARCH ... PRIMARY KEY (parent_id=?)).
- `db/ancestors.sql` and `db/descendants.sql`: the recursive queries use `UNION` on the id alone, so they stop on a loop. A two-person loop (1 to 2 to 1) returned 1 ancestor and finished. The result is correct only while the data is a tree, which family.db is (no cycles, longest chain 14 people). A loop in the data would still make descendants look wider than they are.
- `app/db.py`: `PRAGMA foreign_keys = ON` runs on every connection the app opens, and the cascade works through `delete_person`. An in-memory copy of family.db removed the 4 links of a sample person through this path.
- `family.db`: 0 foreign-key violations, 0 orphan rows, 0 self-links, 0 cycles, and no person without a parent or child link.
- `tests/test_people.py`: both tests pass (2 passed). test_delete_cascades exercises the pragma path, so it would fail if `connect` dropped the setting.

## Not checked
- The Flask front end is not in this repo, so whether it opens its own connections is unknown.
- No GEDCOM file was available. The SUBM and REPO finding was reproduced on a small file made for the test.
- family.db was read through a read-only connection. The delete was run on an in-memory copy, and the import was not run.
- The re-import duplication and the self-link drop were confirmed by reading the code and one parse test, not by a full import.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

Your friend is half right, and the half he has wrong matters for what he recommends.

He is right that SQLite leaves foreign keys off on a new connection. On a plain connection, deleting a person leaves 4 dangling parent_of rows in a test on a copy of your tree. He is wrong that this happens in your app: app/db.py turns `PRAGMA foreign_keys = ON` on for every connection, so the ON DELETE CASCADE in db/schema.sql does run through delete_person. Your family.db has 0 foreign-key violations and 0 orphan rows. You do not need a cleanup job or triggers. The one thing to keep in mind is any code that opens its own connection outside app/db.connect(). The Flask front end is not in this repo, so I could not check it.

Nothing serious in app/, db/ or tools/. Top findings:
- medium, `parse` (tools/import_gedcom.py): a SUBM or REPO record after the last person renames that person. Reproduced on a small file. Your real files may not have that layout, so it depends on what the relatives send.
- low, `delete_person`: the cascade depends only on the connection setting. Deleting the rows in the function itself would make it independent of that.
- low, `load`: a GEDCOM self-link is dropped silently, and importing the same file twice doubles the tree. The README's "once per file" rule is not enforced by the code.

The recursive ancestor and descendant queries stop even on a loop, and the indexes match their joins.

Files:
- /run/work/docs/graph/ROAST.md
- /run/work/findings.json

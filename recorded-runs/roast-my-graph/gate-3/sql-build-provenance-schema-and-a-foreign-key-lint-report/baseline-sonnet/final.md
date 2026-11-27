Don't add that index. The one FK warning is a false alarm for this database, and the index would cost you real money and write throughput.

Why: FK001 says every DELETE or key UPDATE on `blob` will scan `artifact_input` for referencing rows. But `blob_no_update_or_delete` makes those operations impossible, and the README says blob rows are never changed or removed, so that scan never happens. Nothing in `queries/` looks up `artifact_input` by `input_digest` either, because impact questions run in the warehouse. So the index would never be read. It would still be a second btree on an 11 billion row table taking about 4 million inserts an hour, and a plain `CREATE INDEX` in a migration would block those inserts for hours. I'd put a comment on the foreign key and suppress FK001 for it, and revisit only if a query that needs the index is added.

Things I would fix before go-live:

1. `queries/record_step.sql`: three separate inserts with the artifact id passed from one to the next. There is nothing saying they run in one transaction, so a crash can leave an artifact with no inputs. `artifact` also has no unique key on `(build_id, step)`, so a retried step creates a duplicate artifact. Put the three statements in one transaction and make retries idempotent.
2. `queries/producer_of_blob.sql`: no LIMIT. Identical content has the same digest, so a common blob can have millions of producers, and the build page would try to return them all. Add `ORDER BY ... LIMIT`.
3. Immutability depends on triggers only, and `db/` defines no roles. If the service connects as the table owner, it can drop the triggers. Add an insert and select only role.
4. `artifact_input` has no partitioning or retention plan at 11 billion rows and growing. This is the thing that will hurt later.
5. Smaller: `blob.size` has no `CHECK (size >= 0)` and cannot be fixed later because rows are immutable. `blob_is_immutable` reads `OLD.digest` in the TRUNCATE trigger, where there is no row, so the error text is unhelpful (the truncate is still blocked). `artifact_build` would be better as `(build_id, id)` for the ORDER BY.

All 8 items are in findings.json in the repo root, ready to paste into the tracker. I read the files only; nothing was run against a database.

# Roast: provenance-db (db/, queries/) before go-live

Verdict: Nothing serious, so do not add the index the FK linter suggests; the only thing I found is a low-severity cosmetic bug in the error message of the TRUNCATE trigger.

Judged against:
- Engine: PostgreSQL 16 (README.md).
- Sizes: blob 2.3 billion, artifact 900 million, artifact_input 11 billion, build 40 million (README.md).
- Writes: each build step inserts one blob, one `artifact` and one `artifact_input` row per input, about 4 million `artifact_input` rows an hour at peak (README.md, queries/record_step.sql).
- Reads here: `queries/inputs_of_artifact.sql`, `queries/blob_known.sql` (while building), `queries/artifacts_of_build.sql`, `queries/producer_of_blob.sql` (build page). Impact questions ("which builds consumed this input?") run in the analytics warehouse on a nightly copy, not here (README.md).
- Invariant: blob rows are never changed or removed; `db/triggers.sql` enforces it (README.md).

## Findings

### low: `blob_is_immutable`
The trigger refuses to let anyone truncate the blob table, then reports that the digest it refused to truncate is NULL. It is a very polite bouncer who forgot the name of the guest.
Problem: When someone runs `TRUNCATE blob CASCADE` (the one way past the foreign-key refusal), `blob_no_truncate` correctly blocks it, but the shared function reads `OLD.digest`, which does not exist in a statement-level trigger, so the message is `blob rows cannot be truncate (digest <NULL>)`. I ran it on PostgreSQL 16.13 and the table kept its row. Only the wording is wrong.
Fix: Give the statement trigger its own message, for example a separate function `blob_no_truncate_fn()` that does `RAISE EXCEPTION 'blob rows cannot be truncated';`, and point `blob_no_truncate` at it. Optional, no migration.

## Holds up
- `artifact_input` with no index on `input_digest` (the FK001 warning): the linter's reason is that every DELETE on `blob`, and every UPDATE of `blob.digest`, scans `artifact_input` to look for referencing rows. `blob_no_update_or_delete` makes both statements raise before any foreign-key check, and `blob_no_truncate` blocks TRUNCATE; I confirmed on PostgreSQL 16 that DELETE, UPDATE and TRUNCATE of `blob` all fail. No query in `queries/` looks up `artifact_input` by `input_digest`, because the README sends that question to the warehouse. An index on 11 billion rows would cost hundreds of gigabytes and slow the 4 million inserts an hour to protect statements that cannot happen. Safe as written: suppress FK001 for this foreign key, with the reason "blob rows are immutable (db/triggers.sql)". What would change that: dropping the immutability rule (a retention policy), or moving "which builds consumed this input" queries onto this database; then add `CREATE INDEX CONCURRENTLY artifact_input_digest ON artifact_input (input_digest);`.
- `artifact_input` primary key `(artifact_id, input_digest)`: leads with `artifact_id`, so `inputs_of_artifact.sql` is an index search, and `ON CONFLICT DO NOTHING` in `record_step.sql` makes a retried step idempotent.
- `artifact_build` and `artifact_output`: serve `artifacts_of_build.sql` (`build_id`) and `producer_of_blob.sql` (`output_digest`); `blob_known.sql` uses the `blob` primary key. The other foreign keys the linter checked (`artifact.build_id`, `artifact.output_digest`, `artifact_input.artifact_id`) each have an index leading with that column.
- `record_step.sql`: `ON CONFLICT (digest) DO NOTHING` never fires the update trigger, so re-recording a blob that already exists is safe.

## Not checked
- `record_step.sql` is three statements; the files do not show that the service runs them in one transaction (a failure between them would leave an artifact without its input rows).
- `producer_of_blob.sql` returns every artifact that produced the digest; the same content can be built twice (the blob insert tolerates a conflict), so confirm the build page expects a list.
- Query plans and timings at 11 billion rows: only the schema and triggers were run, on an empty PostgreSQL 16 database.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

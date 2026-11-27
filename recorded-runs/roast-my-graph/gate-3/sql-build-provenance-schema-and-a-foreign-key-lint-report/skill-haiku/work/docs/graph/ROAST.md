# Roast: provenance-db (db/, queries/)

Verdict: Nothing serious for go-live in these files. Do not add the index the FK linter suggests. On 11 billion rows it would block the write path, and the blob immutability trigger means no delete or update ever scans the table it covers. Two low questions about the write path are worth answering before go-live.

Judged against:
- Engine: PostgreSQL 16 (README).
- Write path: each build step inserts one blob, one artifact and one artifact_input row per input, about 4 million artifact_input rows an hour at peak (README, `queries/record_step.sql`).
- Read path: `inputs_of_artifact.sql`, `blob_known.sql`, `artifacts_of_build.sql`, `producer_of_blob.sql` (README). Impact questions run in the analytics warehouse, not here (README).
- Sizes: blob 2.3 billion, artifact 900 million, artifact_input 11 billion, build 40 million (README).
- Immutability: blob rows are never updated or deleted, and `blob_no_update_or_delete` and `blob_no_truncate` enforce it (README, `db/triggers.sql`).

## Findings

### low: `record_step.sql`
Question to confirm: is a retried step safe?
Problem: The file is three statements with `$5` supplied by the caller and no stated transaction. `artifact` has no unique key on (build_id, step), and each run takes a fresh bigserial id. A retry after a commit that the farm did not see duplicates the step on the build page and gives `producer_of_blob.sql` two producers. A run that stops after the artifact insert leaves an artifact with no inputs.
Fix: Confirm how the farm calls this file. Run the three statements in one transaction, with the artifact id from RETURNING. If each step produces exactly one artifact, add a unique constraint on `artifact (build_id, step)`, and make the insert idempotent.

### low: `artifact_input`
Question to confirm: where do source blobs and build rows come from?
Problem: `record_step.sql` inserts only the output blob, but `artifact_input.input_digest` references `blob.digest`, and `artifact.build_id` references `build.id`. The repo has no insert path for source files that are not build outputs, or for build rows. If the first step reads raw sources, its insert fails the foreign key at go-live.
Fix: Confirm where source blobs and build rows are recorded. If that happens outside this repo, document it in the README beside the write path. If not, add an ingest step that inserts them in the same transaction as the first `record_step`.

## Holds up
- `artifact_input.input_digest` (FK001 in `lint/fk_report.txt`): the linter is right that no index leads with this column. The index is not needed for go-live. Every delete or update of `blob` is stopped by the BEFORE triggers in `db/triggers.sql` before the foreign key check runs, so nothing scans `artifact_input` on that path. The index would be a non-concurrent build over 11 billion rows, which takes a lock that blocks inserts for the whole build, and no read query in `queries/` filters on `input_digest`. Would change if the immutability triggers were dropped or disabled, or if a query started filtering on `input_digest`. If a later need appears, build it with CREATE INDEX CONCURRENTLY outside a transaction.
- `artifact_input` primary key `(artifact_id, input_digest)`: serves `inputs_of_artifact.sql`, which filters on the leading column `artifact_id`.
- `artifact_output` on `artifact (output_digest)`: serves `producer_of_blob.sql`.
- `artifact_build` on `artifact (build_id)`: serves `artifacts_of_build.sql`, which then sorts by `id`. Would change if a build had enough artifacts for that sort to matter.
- `blob` primary key on `digest`: serves `blob_known.sql` as an exact-match search.
- `ON CONFLICT (digest) DO NOTHING` in `record_step.sql`: content addressing means a repeated digest has the same bytes, so skipping the insert is correct.

## Not checked
- No PostgreSQL server was available, so no plans were read and the trigger ordering (BEFORE triggers run before the foreign key's AFTER checks) was not run.
- How the build farm calls `record_step.sql` (transaction boundaries, retries) is not in the repo.
- Source blob and build row inserts were searched for across `db/` and `queries/` only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

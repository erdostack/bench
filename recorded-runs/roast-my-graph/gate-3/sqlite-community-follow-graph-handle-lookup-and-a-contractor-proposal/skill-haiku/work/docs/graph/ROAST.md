# Roast: commons (migrations/, queries/)

Verdict: Nothing serious. The contractor is wrong about the handle lookup: it is not a full table scan, because migration 0004 already builds an index on exactly the expression the query uses. The 3 days for `handle_lower`, triggers and a backfill are not needed. Two low questions remain about the follow timestamps and about case folding.

Judged against:
- Handles are case-insensitive, `account_by_handle.sql` runs on every profile view, and `followers_page.sql` pages through followers (README.md, lines 5-7).
- About 200,000 accounts and 3 million follows in production; social.db is a 20,000-account sample (README.md, line 10).
- The contractor's claim: `account_by_handle.sql` wraps the column in `lower()`, which "always prevents index use", so every view scans all 200k accounts; proposed fix is a `handle_lower` column with triggers, an index and a backfill, estimated at 3 days (docs/contractor-notes.md, lines 3-6).
- The index that exists: `CREATE UNIQUE INDEX account_handle_ci ON account(lower(handle))` (migrations/0004_handle_lookup.sql, line 2).

Measured (read-only on social.db, SQLite 3.53.1): `EXPLAIN QUERY PLAN` for the handle query reports `SEARCH account USING INDEX account_handle_ci (<expr>=?)`, not a scan. The followers query reports `SEARCH f USING COVERING INDEX follow_by_followee (followee_id=? AND (created_at,follower_id)<(?,?))` with no temporary sort. Walking the pages for the most-followed sample account (31 followers) returns the same rows, in the same order, as one full query. The sample has no duplicate handles and no 1970 timestamps.

## Findings

### low: `0003_follow_created.sql`
Question to confirm: did any follow row exist when this migration ran?
Problem: `ADD COLUMN created_at ... DEFAULT '1970-01-01T00:00:00Z'` gives every existing follow that timestamp. If production had follows before this migration (the README says it has 3 million), those rows are stamped 1970 and `followers_page.sql` orders them by follower_id, not by when they happened. The files do not say when the migration ran, and the sample has no such rows, so this is a question, not a shown defect. The same default also fills in silently for any future insert that leaves `created_at` out; no writer is in the repo.
Fix: Confirm the migration ran on an empty follow table, or backfill the real times from any source that has them. Make the column `NOT NULL` without a default for new writes, or have the writer always set it.

### low: `account_handle_ci`
Question to confirm: which characters can a handle contain?
Problem: `lower()` in SQLite folds only ASCII letters unless an ICU build is used, and the files do not say which characters handles may use. If a handle can contain non-ASCII letters, "Émile" and "émile" would be two accounts, and the README's case-insensitive rule would not hold. The sample has no non-ASCII handles, so this is a question, not a defect shown.
Fix: Check the handle rules for allowed characters. If non-ASCII is allowed, decide on the folding rule and apply it in the application before both the index and the query use the same value. Verify ICU behaviour on the production SQLite build first, since this is not in the repo.

## Holds up
- `account_by_handle.sql` with `account_handle_ci`: the query expression `lower(handle)` matches the index expression exactly, so SQLite searches the index. The contractor's premise does not hold.
- `followers_page.sql` with `follow_by_followee (followee_id, created_at, follower_id)`: the index leads with the filtered column and the row comparison uses it as a range; the descending order matches the index scanned backwards, so there is no sort step.
- The unique index on `lower(handle)` enforces the case-insensitive rule the README states, so duplicate handles cannot be written.
- `follow` keyed by `(follower_id, followee_id)` with `WITHOUT ROWID`: the primary key serves lookups by follower; the index above serves lookups by followee.

## Not checked
- Production timings were not measured; social.db is a 20,000-account sample. The plans show index use, not speed at 200,000 accounts.
- Whether any follow rows existed before migration 0003 was applied is not in the files.
- SQLite's ASCII-only `lower()` is written from long-stable behaviour and was not run against an ICU build.
- No writer code is in the repo, so the timestamp default and the uniqueness of handles on insert were not traced through the application.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

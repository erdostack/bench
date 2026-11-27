# Roast: commons migrations/ and queries/

Verdict: Sound. The contractor is wrong about the handle lookup, so the 3 days are not needed: `queries/account_by_handle.sql` already uses an index, `account_handle_ci` from `migrations/0004_handle_lookup.sql`, and I confirmed it on the sample. The list of findings is empty.

Judged against:
- Engine: SQLite (README.md); the sample ran on SQLite 3.53.1 through Python's `sqlite3`, opened read-only. Version of production: not stated. No `docs/graph/CONTEXT.md`.
- Size: about 200,000 accounts and 3 million follows in production; `social.db` is a sample with 20,000 accounts and 259,811 follows (README.md, counted).
- Interactive path: `account_by_handle.sql` "runs on every profile view", then `followers_page.sql` pages through the followers (README.md).
- Invariant: "Handles are case-insensitive: @Ana and @ana are the same account" (README.md).
- Schema: the migrations applied in order (README.md); the sample's `sqlite_schema` matches them exactly.
- The claim under test: docs/contractor-notes.md, item 1.

## Findings

None.

An empty list is rare enough to deserve a moment: a schema with a case-insensitive uniqueness rule that is enforced by the database, a lookup that uses the very expression it is declared on, and keyset pagination that finishes without sorting anything. The one piece of expert advice in the folder is the one that is wrong.

## Holds up
- `account_handle_ci`: the contractor's note says "a function on a column always prevents index use in SQLite". That is not true for an index on an expression. `CREATE UNIQUE INDEX account_handle_ci ON account(lower(handle))` indexes exactly `lower(handle)`, and `WHERE lower(handle) = lower(:handle)` in `account_by_handle.sql` is the same expression. I ran `EXPLAIN QUERY PLAN` on the sample: `SEARCH account USING INDEX account_handle_ci (<expr>=?)`, not a scan, and the plan does not depend on the table size, so the 200,000 accounts of production behave the same. The same index is what enforces "@Ana and @ana are the same account" (it is `UNIQUE`), which is the other half of what `0004_handle_lookup.sql` says it is for.
- The proposal itself (a `handle_lower` column, triggers on INSERT and UPDATE, an index, every handle query rewritten, 3 days with backfill) would copy the lookup key into a second column and add triggers to keep it in step, which is the exact job the expression index already does with nothing to maintain. It would also leave every other writer one trigger away from drift. It buys nothing the files show a need for.
- `follow_by_followee` with `followers_page.sql`: the query filters `followee_id = :account_id`, orders by `created_at DESC, follower_id DESC` and compares the pair `(created_at, follower_id)`, and the index is `(followee_id, created_at, follower_id)`. The sample plan: `SEARCH f USING COVERING INDEX follow_by_followee (followee_id=? AND (created_at,follower_id)<(?,?))` and `SEARCH a USING INTEGER PRIMARY KEY (rowid=?)` for the join, with no temp b-tree for the sort. A page reads 50 index entries and 50 account rows, whatever the number of followers.
- `follow` primary key `(follower_id, followee_id)` WITHOUT ROWID: serves "who does X follow" by its leading column and rejects duplicate follows; the reverse direction (who follows X) is `follow_by_followee`. The `CHECK (follower_id <> followee_id)` stops self-follows.
- `0003_follow_created.sql`: the `DEFAULT '1970-01-01T00:00:00Z'` only labels follows that existed before the column; the sample has none (0 rows with that value) and keyset paging still works for ties because `follower_id` breaks them. Production data: not stated, so not a finding.

## Not checked
- Production data and plans: I only had the 20,000-account sample. A sample shows plan shape, not speed; the plan shape (a search by an index, not a scan) is what decides the question, and the stated size does not change it.
- Handles with non-ASCII letters: SQLite's built-in `lower()` folds ASCII letters only (`lower('ÉLODIE')` gives `Élodie`), so "@Élodie" and "@élodie" would count as different accounts. The sample has no non-ASCII handle and the files do not say whether production allows them, so this is a question to confirm, not a defect.
- The sample's `PRAGMA foreign_keys` is off on a new connection (as always in SQLite); whether the application switches it on is not in these files. The sample has no orphan follows.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

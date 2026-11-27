# Roast: chirp storage (db/, app/)

Verdict: Not ready for signups. The handle lookup can't keep up at the stated size. Every @mention and every signup scans the whole `account` table, because the handle column is case-sensitive while every lookup is written as case-insensitive. The rest is sound, apart from a timestamp that has no time of day and two small questions.

Judged against:
- SQLite 3.45 through Python `sqlite3`, WAL mode, one writer process and a pool of readers (`README.md`). The sample ran on SQLite 3.53.1.
- 1.2 million accounts at launch, 40 million follow edges (`README.md`). `chirp.db` holds 120,000 accounts, 600,000 follows, 60,000 posts and 60,064 mentions, so it is a tenth of the accounts and a sixty-sixth of the follows.
- Handles are case-insensitive: `@Ada`, `@ada` and `@ADA` are the same account (`README.md`; `db/queries/resolve_mention.sql`, comment on line 1).
- Every new post goes through `app/mentions.py`. Peak is about 300 posts a second with two mentions each (`README.md`). The writer is a single process, so these lookups run in the write path.
- Timelines come from `follow` and the followers page reads the other direction (`README.md`).

## Findings

### critical: `account.handle`
Problem: `handle` is declared `TEXT NOT NULL UNIQUE` with the default BINARY collation, so `db/queries/resolve_mention.sql` and `db/queries/handle_taken.sql`, which both filter `handle = :handle COLLATE NOCASE`, cannot use the unique index. In the sample, `EXPLAIN QUERY PLAN` reports `SCAN account USING COVERING INDEX sqlite_autoindex_account_1`. One lookup took about 8.8 ms on 120,000 rows. Scaled linearly to 1.2 million rows that is roughly 90 ms, and at the stated peak `app/mentions.py` does 600 lookups a second, so it needs roughly 50 seconds of scanning per second in a single writer. It cannot finish at the stated size. The same column also lets `@Ada` and `@ada` both be stored, although the README says they are one account. Only `app/signup.py` prevents this, and nothing in the files covers the 1.2 million migrated beta accounts.
Fix: Declare the column with the collation the lookups use, then keep the index and the constraint in one place: `handle TEXT NOT NULL COLLATE NOCASE UNIQUE`. SQLite cannot change a column's collation in place, so rebuild `account` (create the new table, copy, drop, rename) in one transaction. Before the rebuild, run `SELECT LOWER(handle) FROM account GROUP BY 1 HAVING COUNT(*) > 1` on production and resolve any rows it returns. Tested in memory on SQLite 3.53.1: with the column declared `COLLATE NOCASE`, both queries plan as `SEARCH account USING COVERING INDEX ... (handle=?)`, `'ADA'` is rejected as a duplicate of `'Ada'`, and the stored spelling is kept. Under SQLite 3.45 the plan is expected to match, but that was not run.

### medium: `post.posted_at`
Problem: All 60,000 `posted_at` values in `chirp.db` are dates only (`2026-11-21`, length 10), with no time of day. `db/queries/timeline.sql` orders by `p.posted_at DESC` and keeps 50 rows. Any posts from the same day tie, and the database picks among the ties arbitrarily, so the timeline can show an arbitrary 50 of that day's posts rather than the latest 50. This only bites when a viewer's followed accounts post more than 50 times in one day. The files do not state that volume, so this is a medium at most.
Fix: Store the full timestamp in ISO 8601 with time and an offset (for example `2026-11-21T14:03:09Z`), and add a tiebreaker to the query: `ORDER BY p.posted_at DESC, p.id DESC`. Existing rows need a backfill from whatever source has the time of day; the date alone cannot recover it.

### low: `HANDLE`
Problem: The regex in `app/mentions.py` matches any `@word`, including the part after the `@` in an email address. `ada@example.com` resolves `example` if an account by that name exists. Nothing in the files says whether emails should be ignored, so this is a question to confirm and not a defect.
Fix: Confirm the product rule. If emails should not count, add a lookbehind for a word character, for example `(?<![A-Za-z0-9_])@([A-Za-z0-9_]{2,30})`, and test it on a sample email.

### low: `db/schema.sql`
Problem: `follow`, `post` and `mention` declare `REFERENCES` clauses, but `PRAGMA foreign_keys` is off on a new connection and no file in the repo turns it on. The sample has no orphan rows. The post and account write paths are not in the repo, so whether a delete can leave one cannot be checked. This is a question to confirm.
Fix: Confirm that every connection that writes runs `PRAGMA foreign_keys = ON`. If the answer is no, that is the change to make, and it should be checked with `PRAGMA foreign_key_check` before the change.

## Holds up
- `follow` `PRIMARY KEY (follower_id, followee_id)`: `db/queries/timeline.sql` starts with `SEARCH f USING PRIMARY KEY (follower_id=?)`. The key leads with the lookup column, so it is searched.
- `follow_by_followee (followee_id, follower_id)`: `db/queries/followers.sql` plans as `SEARCH f USING COVERING INDEX follow_by_followee (followee_id=?)`, so the followers page does not scan. The index is in the other direction on purpose.
- `post_by_author (author_id, posted_at)`: the timeline's second step, `SEARCH p USING INDEX post_by_author (author_id=?)`. Nothing else in the timeline needs a table scan.
- `mention_by_account (account_id, post_id)`: `db/queries/mentions_of.sql` plans as a covering search, and the index already provides the `ORDER BY post_id DESC`, so there is no sort step.
- `mention` (`post_id`, `account_id`): a many-to-many link keyed by the pair, with no properties beyond the keys, read by pair in `app/mentions.py` and by account in `db/queries/mentions_of.sql`. It is the link itself in relational form, not a node between two others. If mentions gain their own data (a position in the text, a notified time) it should still be keyed by the pair.
- `app/signup.py` `create_account`: the check and the insert are not atomic, but the README says the storage has one writer process, so no other insert can land between them. This is sound for the stated topology. A second writer process would make it a defect.
- `followers.sql` has `LIMIT 100` with no `ORDER BY`: the result is any 100 followers. That is what the query asks for, so nothing to fix.

## Not checked
- The production database was not available. Every result is from the 120,000-account sample. The 90 ms figure is a linear extrapolation from that sample, not a measurement at 1.2 million rows.
- The migration from beta, the post insert path and any account deletion are not in the repo, so the handle duplicates and orphan rows cannot be checked against them.
- The timeline sort (`USE TEMP B-TREE FOR ORDER BY`) has a cost that grows with follows times posts per followee. The sample averages 5 follows and 1.3 posts per author, while the README gives 40 million follows over 1.2 million accounts (about 33 each). The posts-per-author figure at scale is not stated, so the timeline was not rated above medium.
- The NOCASE fix was tested on SQLite 3.53.1 only.
- The sample is smaller than the README scale. Plans were read from it; speed was not judged from it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

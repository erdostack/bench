# Roast: chirp storage layer (db/, app/)

Verdict: not ready for signups as written. One critical: every mention resolves with a full scan of the account table, about 600 scans a second at the stated size. One index fixes it, and the rest is minor.

Judged against: SQLite 3.45, WAL, one writer process and a pool of readers (README.md); 1.2 million accounts, 40 million follow edges (README.md); handles case-insensitive, shown as typed (README.md); about 300 posts/s at peak, two mentions each (README.md); post volume, retention and signup rate: not stated. `chirp.db` is a 120,000-account sample (600,000 follows, 60,000 posts), one tenth of the stated account count; plans were read on it with SQLite 3.53.1.

## Findings

### critical: `resolve_mention.sql`
The mention resolver reads the entire phone book to find one name, 600 times a second, because the index and the query disagree about what the letter A is.
Problem: When `record_mentions` runs `resolve_mention.sql` for each handle in a post at 300 posts/s with two mentions, on 1.2 million accounts, the `COLLATE NOCASE` comparison cannot use the binary `UNIQUE` index on `handle`: the plan is `SCAN account USING COVERING INDEX sqlite_autoindex_account_1`, about 600 full scans/s (about 9 ms each on the 120k sample, so about 90 ms at full size).
Fix: `CREATE UNIQUE INDEX account_handle_nocase ON account (handle COLLATE NOCASE);` Verified on an in-memory copy: plan becomes `SEARCH account USING COVERING INDEX account_handle_nocase (handle=?)`. Check for case-only duplicate handles first (none in the sample). For a fresh schema declare `handle TEXT NOT NULL UNIQUE COLLATE NOCASE`.

### medium: `handle_taken.sql`
Problem: the same NOCASE-against-BINARY mismatch makes every `create_account` call scan all accounts. Signup rate not stated.
Fix: the same `account_handle_nocase` index.

### low: `handle`
Problem: `UNIQUE` is binary, so the database allows `@Ada` and `@ada` as two accounts; only the check in `create_account` prevents it. No such pair in `chirp.db`, one writer process stated: a question to confirm, not a defect.
Fix: the same index; then catch `sqlite3.IntegrityError` in `create_account`.

### low: `timeline.sql`
Problem: reads every post of every followee, sorts, then takes 50. Post volume and retention not stated: a question.
Fix: if post volume is large, add `AND p.posted_at > :since` (served by `post_by_author`) or keep a timeline table written at post time.

### low: `followers.sql`
Problem: `LIMIT 100` with no `ORDER BY` and no paging, so followers beyond the first 100 cannot be reached.
Fix: keyset paging on `follower_id`: `AND f.follower_id > :after ORDER BY f.follower_id LIMIT 100`.

## Holds up
- `follow`: primary key `(follower_id, followee_id)` serves `timeline.sql` (search on `follower_id`), and `follow_by_followee` serves `followers.sql` (covering search on `followee_id`). Both directions README names are indexed.
- `mention`: a table joining post and account with its own two keys and `mention_by_account`; `mentions_of.sql` is two index searches. The `INSERT OR IGNORE` in `record_mentions` plus `set()` handles repeated mentions of one handle in a post.
- `follow_by_followee`, `mention_by_account`: needed, not duplicates of the primary keys, because the primary keys lead with the other column.
- Foreign keys: `PRAGMA foreign_key_check` on `chirp.db` returns no rows. Enforcement depends on each connection enabling `PRAGMA foreign_keys` and nothing in the repo does, but no dangling row exists and no write path produces one, so this is not filed.

## Not checked
- Ran read-only on the 120,000-account sample (SQLite 3.53.1 here, 3.45 in the README); timings are the sample's, scaled by the README's account count, not measured at 1.2 million. Application code outside `app/` was not provided.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

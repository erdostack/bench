Verdict: not ready for signups as written, because of one critical finding in `db/queries/resolve_mention.sql`. Everything else is minor.

`resolve_mention.sql` looks up handles with `COLLATE NOCASE`, but `account.handle` is indexed with the default binary collation. So every mention resolve is a full scan of `account` (confirmed with EXPLAIN QUERY PLAN on `chirp.db`). The README says 1.2 million accounts and about 300 posts/s with two mentions each, which is about 600 full scans a second. The sample (120,000 accounts) takes about 9 ms per lookup, so about 90 ms at full size.

Fix, verified on an in-memory copy of `chirp.db` (plan becomes a SEARCH):
`CREATE UNIQUE INDEX account_handle_nocase ON account (handle COLLATE NOCASE);`
Check first for handles differing only by case (none in the sample).

Other findings (all in `findings.json` in the repo root, ready to paste):
- medium, `handle_taken.sql`: same scan on every signup. Same index fixes it.
- low, `handle`: the schema lets `@Ada` and `@ada` coexist, which the README forbids. Only the check in `create_account` stops it. No such pair in the data. The same index fixes it.
- low, `timeline.sql`: reads all posts of all followees before `LIMIT 50`. Post volume is not stated, so this is a question to confirm.
- low, `followers.sql`: `LIMIT 100` with no order or paging, so followers past 100 are unreachable.

Holds up: both `follow` directions are indexed, `mention` is a sound join table, and `foreign_key_check` is clean on the sample.

The full write-up is in `docs/graph/ROAST.md`. Nothing under review was modified.

# Roast: audience job (schema.sql, queries/, jobs/nightly_audience.py)

Verdict: Nothing serious, and no, do not apply the linter's suggested fix. `queries/extended_audience.sql` already terminates on cyclic data because its recursive CTE uses `UNION` over the account id alone: an id that was already produced is not produced again, so mutual follows cannot loop. The suggested depth column would remove that protection and make the query about 280 times slower on the sample. The findings list is empty.

Judged against:
- Engine: SQLite 3.53.1 through Python 3.13 `sqlite3` (run here); the README does not state an engine or version.
- Size: about 300,000 accounts and 4 million follows in production; `audience.db` is a 6,000-account sample with 49,497 follows (README.md; counted on the sample).
- Workload: ~30 brand accounts, one extended-audience query each, nightly at 02:00, "nobody waits on it" (README.md, `jobs/nightly_audience.py`).
- Shape of the data: "Most follows are mutual" (README.md). On the sample, 39,088 of 49,497 follow rows have a reverse row (79%), so cycles are everywhere.
- Writers and rates: not stated beyond the nightly job.

## Findings

None.

The linter looked at a recursive CTE, saw a mutual-follow graph, and screamed "infinite loop". It is a lovely theory. The CTE has a one-column working table and a `UNION`, which means it has already seen everyone in the room and refuses to invite them twice. The fix it proposes is to hand each guest a numbered wristband so that they all look new again.

## Holds up
- `audience` (the recursive CTE in `queries/extended_audience.sql`): safe as written. The recursive rows carry the id alone and the CTE uses `UNION`, not `UNION ALL`, so a row already in the result is dropped and the walk ends when no new account is reachable. A cycle cannot revisit anything. I ran it read-only against `audience.db` for brand accounts: it finished in about 0.05 s each (5,999 extended followers, the whole sample) and its result matched an independent breadth-first walk for all 30 brand accounts, 0 mismatches. The plan is a search on `follow_followee`, not a scan. What would change this: someone adds a column to the CTE (a depth, a path) or switches to `UNION ALL`. Then each row is new and only the guard stops it.
- The linter's suggested fix (`depth` column and `WHERE a.depth < 100`): do not apply. With the depth column, `UNION` no longer removes repeats, because the same account at depth 3 and depth 4 are different rows. On the sample, one brand account went from 5,999 distinct accounts in about 0.05 s to 586,645 rows in about 13.8 s, for the same answer. Production is about 50 times as many accounts and 80 times as many follows, so the rows grow with the reachable set times the depth cap (up to 100) per brand account, for 30 brand accounts. The cap would also silently cut off any audience more than 100 hops deep, which nothing in the files asks for. If CI must be green, exempt this one query in the linter's config or with an inline suppression, with the reason above, since the guarantee comes from `UNION` over the id alone. Cheap insurance that keeps the guarantee: nothing needed; a comment above the `UNION` saying why it must stay `UNION` would stop a later edit from breaking it.
- `follow_followee` index on `follow(followee_id, follower_id)`: the recursive step and `queries/direct_followers.sql` both look up by `followee_id`, and the primary key `(follower_id, followee_id)` only serves `follower_id`. The index is what the plan uses, and it covers the step.
- `follow` primary key and `CHECK (follower_id <> followee_id)`: no duplicate or self follows, so the count in `direct` is a count of distinct followers. On the sample no follow row points at a missing account.
- `queries/mutuals.sql`: joins the reverse row through the primary key and filters on the indexed `followee_id`. The job does not call it; it is not part of this CI failure.
- `audience_report` primary key `(account_id, run_date)` with `INSERT OR REPLACE` in `jobs/nightly_audience.py`: rerunning the job on the same day replaces the row instead of duplicating it.
- `SELECT id FROM account WHERE brand = 1` in `jobs/nightly_audience.py`: reads the account table once a night for about 30 rows. A scan at 300,000 rows in a batch nobody waits on is not a cost worth an index.

## Not checked
- Production data: only the 6,000-account sample was run. The cost of the suggested fix at 300,000 accounts and 4 million follows is extrapolated from the sample, not run; the guarantee that the original terminates comes from the `UNION` semantics and the sample run.
- The linter itself (`sqlguard`) is not installed; I read its output in `ci/sql-lint.txt` only and do not know its exemption syntax.
- `PRAGMA foreign_keys` is not set by the job, but the job only writes ids it just read from `account`, so nothing in the files depends on it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

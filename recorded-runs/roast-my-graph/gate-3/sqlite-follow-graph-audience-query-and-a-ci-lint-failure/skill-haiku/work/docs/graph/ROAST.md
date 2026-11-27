# Roast: queries/extended_audience.sql (audience job)

Verdict: Do not apply the linter's suggested fix. The flagged recursion terminates: `UNION` keeps only one row per account id, so mutual follows cannot make it loop. The suggested depth counter does not stop a loop; it changes the count, and on the sample it inflates a brand's extended audience from 5999 to 586644. Sound as written; nothing serious.

Judged against:
- Brand accounts: about 30, each traversed once per nightly run (`README.md`, `jobs/nightly_audience.py`).
- Production size: about 300,000 accounts and 4 million follows; the sample is 6,000 accounts and 49,497 follows (`README.md`; sample counted read-only in `audience.db`).
- Follow shape: most follows are mutual (`README.md`); the sample has 19,544 mutual pairs.
- Schedule: nightly at 02:00, nobody waits (`README.md`).
- Engine: SQLite 3.53.1 through Python 3.13 `sqlite3` (`references/engines.md`, run on this machine).
- Keys and indexes: `follow` primary key (follower_id, followee_id); `follow_followee (followee_id, follower_id)` (`schema.sql`).

## Findings

None.

## Holds up
- `audience` (`queries/extended_audience.sql`): the recursive term is `UNION`, so a row whose id was already emitted is discarded and the recursion stops once no new accounts appear. The set is finite (one row per account), so mutual follows are harmless. Run on all 30 brand accounts of the sample, the query finished in 2.25 s total with 5999 each. This would change if the recursive term used `UNION ALL`, or if a counter column were added to the row (see Not checked for the linter's fix).
- `follow_followee` (`schema.sql`): the plan for the recursive step is `SEARCH f USING COVERING INDEX follow_followee (followee_id=?)`, so each step is an index lookup. Without it the join would scan `follow` at every step.
- `count(*) - 1` (`queries/extended_audience.sql`): the seed row (the brand itself) is always in the result, so subtracting one is correct. The sample has no brand with zero followers, so the count is never negative.
- `direct_followers.sql`: the count is answered by `follow_followee` (followee_id leads), so the direct count is an index search too.
- `audience_report` primary key (account_id, run_date) with `INSERT OR REPLACE` (`jobs/nightly_audience.py`): a re-run on the same day replaces rows instead of duplicating them.

## Not checked
- The production run was not measured. The sample finishes in about 0.1 s per brand; a 300,000-account, 4-million-follow graph was not built, so the time the nightly job takes at production size is not known from these files.
- The linter's suggested fix was run on the sample only, in read-only mode, for four brands in full and as a timed run. Its ~586,000 figure is the non-distinct count of (id, depth) rows. A `count(DISTINCT id)` variant gives 5999 but took about 9 to 14 s per brand on the sample, so it is not a practical replacement.
- `mutuals.sql` was read but not run; it is not called by the nightly job.
- The sqlguard rule RECURSIVE-CTE-UNBOUNDED was judged against the query text only; the linter itself was not run.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

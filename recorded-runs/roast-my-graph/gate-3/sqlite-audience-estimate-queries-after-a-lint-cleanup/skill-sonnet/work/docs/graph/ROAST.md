# Roast: sql/audience.sql and sql/schema.sql

Verdict: Yes, something is wrong, and it is the number the advertisers are asking about: `second_degree_reach` has counted every route to an account instead of every account since the SQ214 "DISTINCT is expensive" cleanup on 2026-10-02, so it overstates reach, and the quotes are priced from it. One critical finding; the other queries and the schema are fine.

Judged against:
- Engine: SQLite; library version 3.53.1 on this machine. Production version: not stated.
- Meaning: `second_degree_reach` is the number of distinct accounts two follows away, not counting the account itself, and the promoted-post quote is priced from it per thousand accounts, "straight onto the invoice" (README.md). `first_degree_reach` is the number of accounts it follows (README.md).
- Change history: In October everything the linter flagged under SQ214 was cleaned up (README.md); `-- 2026-10-02: SQ214 cleanup, dropped DISTINCT` (sql/audience.sql).
- Sample: social.db has 3,000 accounts and 64,360 follows, ids replaced (README.md; counted). Production size: not stated.
- Workload and write rate: not stated.

## Findings

### critical: `second_degree_reach`
A linter has been paid, in invoice money, to be afraid of one keyword. DISTINCT was the only line in the file saying "once".
Problem: When a promoted-post quote is priced from `second_degree_reach`, the query counts `f2.followee` once per route: an account followed by three of the accounts you follow is counted three times. The README says the number is distinct accounts and goes straight onto the invoice. On social.db, all 3,000 accounts return a different number from `count(DISTINCT f2.followee)`; the totals are 1,351,082 against 761,967, and single accounts are overstated up to about 4 times (account 43: 801 against 206; account 241: 931 against 360). This started with the 2026-10-02 edit, the autumn the advertisers began to complain.
Fix: Put DISTINCT back (SQLite):
```sql
SELECT count(DISTINCT f2.followee) AS reach
FROM follows f1
JOIN follows f2 ON f2.follower = f1.followee
WHERE f1.follower = :account
  AND f2.followee <> :account;
```
I ran it on account 43 and 241: 206 and 360. The query plan is unchanged (both joins search the primary key). Remove the 2026-10-02 comment, exempt this statement from SQ214 with the reason, add a test with a small graph where two routes lead to the same account, and re-check the quotes issued since 2026-10-02: the ones that were overstated need correcting or crediting.

## Holds up
- `first_degree_reach`: a count of `follows` rows by `follower`; the primary key `(follower, followee)` makes each row one account, so no DISTINCT is needed, and the lookup is an index search.
- `mutuals`: pairs each follow with its reverse by primary key; `(follower, followee)` is unique, so a mutual cannot appear twice. Plan: search by primary key and covering index `follows_followee`.
- `recent_followers`: searches `follows_followee` by `followee` and sorts the matches by `since` with a temporary B-tree. The most any account has in the sample is 216 followers; production size is not stated, so I did not file it. What would change this: accounts with millions of followers on an interactive page.
- `follows`: composite primary key plus `CHECK (follower <> followee)` and the reverse index `follows_followee (followee, follower)`; both directions are served, and `WITHOUT ROWID` fits a table whose only lookups are by that key.
- `account.handle UNIQUE`: makes handles unique and searchable.

## Not checked
- The quotes themselves and the tool that prices them, which are not in the repo; I cannot say how many quotes were affected.
- Production data volume and SQLite version; I measured only social.db.
- Whether the quote uses `second_degree_reach` before or after any other adjustment.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

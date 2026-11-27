# Roast: audience queries (sql/audience.sql, sql/schema.sql)

Verdict: Critical. `second_degree_reach` counts paths, not accounts. Since the 2026-10-02 SQ214 cleanup dropped `DISTINCT`, an account reached through two of the accounts it follows is counted twice. The README says the number is distinct accounts and that it goes straight onto the invoice. On social.db every one of the 3,000 accounts is overcounted: the sum is 1,351,082 as written against 761,967 distinct, and account 43 gets 801 where the distinct count is 206. The advertisers are right, and the files show where.

Judged against:
- `second_degree_reach` is the number of distinct accounts two follows away, not counting the account itself. The promoted-post quote is priced from it, per thousand accounts, and the number goes onto the invoice (README.md, lines 6-8).
- `first_degree_reach` is the number of accounts it follows (README.md, line 9).
- The October cleanup removed what linter rule SQ214 ("DISTINCT is expensive, avoid it") flagged (README.md, lines 11-12; sql/audience.sql, line 5).
- Sample sizes from social.db (checked by running it, not stated in the README): 3,000 accounts, 64,360 follows, the most followers any account has is 216, and the most accounts one account follows is 40.
- Engine: SQLite (sql/schema.sql). Checked on SQLite 3.53.1 through Python `sqlite3`.
- Interactive use: the README does not say how often the quote runs.

## Findings

### critical: `second_degree_reach`
Problem: The join counts one row per path. An account followed by two of the accounts an account follows appears twice, and the query has no DISTINCT or GROUP BY to remove the repeats. Trigger in the shipped data: account 43 follows 35 accounts and its second-degree count is 801, while the distinct count is 206. Across all 3,000 accounts in social.db the written query and the distinct count disagree in every case. The sum over accounts is 1,351,082 as written and 761,967 distinct. The files state the right result (README.md: distinct accounts), so this is not a question of intent.
Fix: Count distinct accounts. Keep the account-itself exclusion as it is:

```sql
SELECT count(DISTINCT f2.followee) AS reach
FROM follows f1
JOIN follows f2 ON f2.follower = f1.followee
WHERE f1.follower = :account
  AND f2.followee <> :account;
```

Tested on social.db against a distinct reference for all 3,000 accounts: it matches on every account, and it runs for all accounts in about 0.4 seconds. If the linter rule has to stay green, the same result comes from `SELECT count(*) FROM (SELECT f2.followee FROM ... GROUP BY f2.followee)`, which also matches the reference. Either way, the quotes issued since 2026-10-02 are overstated and need re-quoting.

### low: `second_degree_reach`
Problem: The README says "accounts followed by the accounts it follows" and also "two follows away". The query counts accounts the account already follows, because nothing excludes them. Read literally, the README includes them. If "two follows away" means only accounts not already followed, the count changes for 2,930 of the 3,000 accounts in social.db. This is a product question, so it is filed as low.
Fix: Confirm with the product owner which reading the quote uses. If it excludes accounts already followed, add `AND f2.followee NOT IN (SELECT followee FROM follows WHERE follower = :account)` to the fixed query.

## Holds up
- `first_degree_reach` (sql/audience.sql, line 2): `follows` has primary key (follower, followee), so the count is one row per follow and is correct as written.
- `mutuals` (sql/audience.sql): the self-join on both directions uses the primary key for the reverse lookup. It returns each mutual follow once.
- `recent_followers` (sql/audience.sql): `follows_followee (followee, follower)` leads with `followee`, so the lookup is a search. The sort by `since` reads every follower of that account; the largest is 216 in the sample, and the production size is not stated.
- `follows` (sql/schema.sql): `CHECK (follower <> followee)` rules out self-follows, and the `second_degree_reach` filter on `f2.followee <> :account` is the only exclusion needed.
- `since` is stored as ISO dates (all 64,360 rows are 10 characters), so ordering by it is correct.

## Not checked
- Production sizes and call rates were not in the repo; the timings above are from social.db only.
- The quote engine that prices per thousand accounts was not in the repo, so how the number is rounded or capped was not checked.
- Quotes already issued were not in the repo, so the size of the overcharge in past invoices was not measured.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

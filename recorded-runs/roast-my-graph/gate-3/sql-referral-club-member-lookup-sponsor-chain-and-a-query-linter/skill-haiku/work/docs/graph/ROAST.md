# Roast: referral club (schema.sql, queries/, against lint/sqlcheck.txt)

Verdict: Sound. Neither of the two sqlcheck warnings has to be fixed before the release: both are false positives on the code as written. The email lookup uses the expression index `member_email_lower`, and the sponsor chain has a `CYCLE` clause that stops the recursion on a loop. The only open item is a low-severity sort on the sponsees query.

Judged against:
- PostgreSQL 16, 2.8 million members; members join through a sponsor, and the member page shows the chain of sponsors back to the founding members (`README.md`).
- Login and the invite form look a member up by email, case-insensitively, a few hundred times a second (`README.md`).
- The sponsor lookup and the sponsees list are not described as hot or batch; their frequency is not stated (`README.md`).
- Email uniqueness is case-insensitive, one account per address (`schema.sql`, comment on `member_email_lower`).
- Sponsor rule: `CHECK (sponsor_id <> id)` on `member`; no other rule on sponsor cycles (`schema.sql`).

## Findings

### low: `queries/sponsored_by.sql`
Problem: `WHERE sponsor_id = $1 ORDER BY joined_at` can use `member_sponsor`, which leads with `sponsor_id`, but the index does not carry `joined_at`, so each sponsor's sponsees are sorted after the lookup. The cost depends on how many sponsees a member has, which is not stated, so this is a question to confirm rather than a defect.
Fix: If the query is hot and some sponsors have many sponsees, replace `member_sponsor` with `CREATE INDEX member_sponsor_joined ON member (sponsor_id, joined_at);` (PostgreSQL 16; not run here). Confirm with `EXPLAIN` that the sort disappears before changing the index. Otherwise leave it as is.

## Holds up
- `member_email_lower`: a unique index on `lower(email)` is an expression index that matches `lower(email) = lower($1)` in `queries/find_member_by_email.sql` exactly. The sqlcheck W012 warning says the index cannot be used; that is not what the files show. The same index also enforces one account per address in any case, as the schema comment says. Confirming with `EXPLAIN` on PostgreSQL 16 would show an index scan rather than a sequential scan; not run here.
- `is_cycle`: the `CYCLE id SET is_cycle USING path` clause in `queries/sponsor_chain.sql` (PostgreSQL 14 and later, so PostgreSQL 16 is fine) marks a row that returns to an id already on its path and stops expanding it, so a loop in the sponsor data ends the recursion. The filter `NOT c.is_cycle` removes those rows from the output. The sqlcheck W031 warning says a cycle makes the query run out of memory; that holds for a recursive CTE without this clause, not for this query. A depth cap would be optional insurance only.
- `member_sponsor`: leads with `sponsor_id`, so the recursive step's `JOIN ... ON m.id = c.sponsor_id` uses the primary key on `member.id` and `sponsored_by` uses this index for its equality filter.
- The sponsor chain adds one row per step on a single parent pointer, so the result grows with the depth of the chain, not with the size of the club.

## Not checked
- No PostgreSQL server was running on this machine (`psql` is present, no server was started), so no `EXPLAIN` or `EXPLAIN ANALYZE` was run; the plan claims above are from the schema and query shape, not from a plan.
- Frequency of the sponsees query and the number of sponsees per sponsor are not stated in the repo.
- The linter's sqlcheck 0.9.4 rules were read from its output only; the linter source is not in the repo.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

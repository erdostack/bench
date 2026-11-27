## Which sqlcheck warnings to fix before the release

Neither. Both warnings are false positives for this schema and these queries, so you don't have to fix either one before release. I checked both on a throwaway PostgreSQL 16 instance and removed it afterwards.

- **W012 (`find_member_by_email.sql`).** The linter says `lower(email)` forces a sequential scan. It doesn't, because `schema.sql` defines the expression index `member_email_lower ON member (lower(email))`. EXPLAIN shows an Index Scan on that index for `lower(email) = lower(...)`. Suppress the warning with a comment that names the index.
- **W031 (`sponsor_chain.sql`).** The linter says the recursive CTE has no depth limit and will run until it runs out of memory on a cycle. The query uses `CYCLE id SET is_cycle USING path`, which stops the recursion at a repeated id. On a four-member chain with a loop (4 to 3 to 2 to 1 to 3) the query returned three rows and finished. Suppress the warning with a comment that names the CYCLE clause.

The real problems are elsewhere, and they matter more than either warning:

- **Cycles can be stored.** The only check on `sponsor_id` is `sponsor_id <> id`, so A sponsoring B and B sponsoring A is accepted. The CYCLE clause then hides the loop silently. Reject a sponsor change that would create a loop, and run a periodic audit.
- **Email is not normalised.** The unique index is on `lower(email)` only, so a stray space creates a second account, and the case-insensitive lookup then misses one of them. Trim on write and make the index match.
- **Smaller items.** `sponsored_by.sql` sorts by `joined_at` with an index that covers only `sponsor_id`, so a sponsor with many sponsees gets an in-memory sort. Nothing sets a delete policy for sponsors, and nothing checks that a sponsor joined before the members they sponsor.

Findings are saved to `findings.json` in the repo root (7 entries, with element, severity, problem and fix for each). The index plan was checked on 200,000 generated members, and the cycle behaviour on a four-member sample. Confirm both on production-sized data before release.

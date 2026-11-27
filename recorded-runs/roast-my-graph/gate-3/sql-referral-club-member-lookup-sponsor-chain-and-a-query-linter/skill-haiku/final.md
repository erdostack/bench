Verdict: Neither sqlcheck warning needs fixing before the release. Both are false positives on the code as written.

- W012 on queries/find_member_by_email.sql says the email index cannot be used. It can: member_email_lower is a unique index on lower(email), which matches lower(email) = lower($1) exactly.
- W031 on queries/sponsor_chain.sql says a cycle makes the recursion run out of memory. The query has CYCLE id SET is_cycle USING path, which stops the recursion when a loop closes, and the output filters those rows. That clause needs PostgreSQL 14 or later, and the README says 16.

The one open item is low: queries/sponsored_by.sql sorts each sponsor's sponsees after the lookup. Whether it matters depends on how many sponsees a member has and how often the query runs, neither of which the repo states. A (sponsor_id, joined_at) index would remove the sort.

Full review: /run/work/docs/graph/ROAST.md
Findings: /run/work/findings.json

No PostgreSQL server was running, so no plan was checked with EXPLAIN; the index and CYCLE conclusions come from the schema and query text.

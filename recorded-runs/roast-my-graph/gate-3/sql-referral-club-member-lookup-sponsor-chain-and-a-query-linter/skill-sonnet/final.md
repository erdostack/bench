Verdict: sound. You do not have to fix either warning before the release; both are false positives.

- W012 (`queries/find_member_by_email.sql`): the linter says an index on `member.email` cannot serve `lower(email)`. `schema.sql` already has `member_email_lower`, a unique index on exactly `lower(email)`, and the query filters on `lower(email) = lower($1)`, so it is an index search, not a scan of 2.8 million rows.
- W031 (`queries/sponsor_chain.sql`): the linter looks for a `depth < N` limit. The query already ends its recursive CTE with `CYCLE id SET is_cycle USING path` and filters `NOT c.is_cycle`, so a loop in the sponsor data stops after one lap. Safe as written on PostgreSQL 16 (`CYCLE` exists from 14). A depth bound would be optional insurance, not a fix; suppressing the warnings with these reasons, or adding the bound, is your call.

Nothing else turned up in `schema.sql` or `queries/`, so `findings.json` is an empty list. I had no PostgreSQL server, so I did not run `EXPLAIN`; it is worth confirming both points once on a copy.

Files:
- docs/graph/ROAST.md
- findings.json (repo root, `[]`)

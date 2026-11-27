Neither warning needs fixing before the release. Both are false positives, and I found nothing in schema.sql or queries/ that blocks the release. I did not run the queries against a database. This is from reading the schema, the queries and the lint output.

**W012, `queries/find_member_by_email.sql`.** The linter says `lower(email)` in the WHERE clause prevents index use. That would be true with a plain index on `email`, but schema.sql has `CREATE UNIQUE INDEX member_email_lower ON member (lower(email))`. The query compares `lower(email) = lower($1)`, which matches that expression index, so PostgreSQL 16 can use it. The same index also enforces one account per address regardless of case. Leave it as it is. If you want to be sure, run EXPLAIN on a production-sized copy and check for an index scan on `member_email_lower`.

**W031, `queries/sponsor_chain.sql`.** The linter wants a `depth < N` limit in the recursive term so a cycle in the data cannot run forever. The query already uses `CYCLE id SET is_cycle USING path`, which stops the recursion when an id repeats. The outer query filters out the repeated row with `NOT c.is_cycle`. A real chain ends at a founding member, whose `sponsor_id` is NULL and joins to nothing. So the query terminates on cyclic data without a depth limit. I would not add one: an arbitrary N could silently truncate a legitimate long chain. If the linter output has to be clean, suppress W031 for this file with a comment saying that CYCLE covers it.

**What I did find** (5 low-severity items in findings.json, none blocking):
- `sponsored_by.sql` orders by a date with no tiebreaker and has no pagination.
- `member_sponsor` could be a composite index (`sponsor_id, joined_at, id`) if big sponsors turn out to be slow.
- The `CHECK` constraint only prevents a member sponsoring themselves. Longer cycles can still be stored, and only the `CYCLE` clause protects `sponsor_chain.sql` from them.
- `email` is not trimmed or validated.
- `sponsor_chain.sql` does a redundant join back to `member` to read the name.

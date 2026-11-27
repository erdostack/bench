# Roast: schema.sql and queries/ (referral club)

Verdict: Sound, and neither warning needs fixing before the release. W012 (`find_member_by_email.sql`) is a false positive because `member_email_lower` is an index on exactly `lower(email)`, and W031 (`sponsor_chain.sql`) is a false positive because the query already has a `CYCLE` clause that stops the walk on a loop. Whether to suppress them in the linter (with the reasons below) or add the cheap extra guard is your call; neither is a defect in the files.

Judged against:
- Engine: PostgreSQL 16 (README.md).
- Size: 2.8 million members (README.md).
- Reads: the member page shows the chain of sponsors back to the founding members (README.md, `sponsor_chain.sql`); login and the invite form look a member up by email, case-insensitively, a few hundred times a second (README.md); the sponsored-members list is `sponsored_by.sql`, rate not stated.
- Constraints: primary key on `member.id`, foreign key `sponsor_id` to `member (id)`, `CHECK (sponsor_id <> id)`, unique index on `lower(email)` (schema.sql).
- Linter: sqlcheck 0.9.4, 2 warnings (lint/sqlcheck.txt).

## Findings

None.

An empty list on a schema with a self-referencing sponsor chain, a case-insensitive email login and a linter that is complaining at both is rare enough that it is worth saying twice: nothing here is wrong. The linter simply cannot see inside the indexes and the `CYCLE` clause.

## Holds up
- `find_member_by_email.sql` (linter W012): the warning says an index on `member.email` cannot serve `lower(email)`. True, and irrelevant: schema.sql creates `member_email_lower`, a unique index on the expression `lower(email)`, and the query filters on `lower(email) = lower($1)`. The column side is the same expression as the index, so the planner can search the index instead of scanning 2.8 million rows. The unique index also enforces "one account per address, whatever the case". What would change this: an index declared on `email` only, or a different expression such as `lower(trim(email))` in the query.
- `sponsor_chain.sql` (linter W031): the warning says there is no `depth < N` and that a cycle runs the query out of memory. The recursive CTE ends with `CYCLE id SET is_cycle USING path`, which makes PostgreSQL stop expanding a row when its `id` has already appeared on that walk, and the outer query drops those rows with `NOT c.is_cycle`. A loop in the sponsor data (A sponsors B sponsors A, which the `CHECK (sponsor_id <> id)` alone does not prevent) therefore ends after one lap. Each step is a primary-key lookup (`m.id = c.sponsor_id`), and the chain is one row per sponsor level. Safe as written. If a depth bound is wanted as optional insurance for very long legitimate chains, `AND c.depth < N` in the recursive term is valid; the stated workload does not need it, and the linter's rule is not evidence of a problem.
- `member_sponsor` / `sponsored_by.sql`: `WHERE sponsor_id = $1` leads with the indexed column, so it is an index search, and it also serves lookups from the foreign key (PostgreSQL does not create an index for a foreign key on its own). The `ORDER BY joined_at` sorts only one sponsor's members.
- `member.sponsor_id`: nullable by design, since founding members have no sponsor, which is where the chain stops.

## Not checked
- No PostgreSQL server was available, so no `EXPLAIN` was run: that `find_member_by_email.sql` uses `member_email_lower` and that the `CYCLE` clause stops a loop rests on documented PostgreSQL behaviour (expression indexes match the same expression; `CYCLE` exists from version 14) that was not executed here. Both are quick to confirm on a copy with `EXPLAIN` and a two-row loop.
- How many members one sponsor can have is not stated; `sponsored_by.sql` sorts that many rows.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

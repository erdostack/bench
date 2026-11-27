# Roast: guild (migrations/, queries/, guild/, guild.db)

Verdict: One real problem, and it is the one you felt: `queries/member_by_handle.sql` scans the whole `member` table on every @mention because it asks for `lower(trim(handle))` while the index is on `lower(handle)`. Change the query to `lower(handle) = lower(:handle)` and it becomes an index search; I ran the plan and the lookup went from about 12 ms to about 0.07 ms on the sample. Nothing else in the files is serious: the mentor lineage query is safe as written. One `high`, one `low`.

Judged against:
- Engine: SQLite 3.53.1 through Python 3.13 (run here); the README does not state an engine version.
- Size: about 350,000 members; `guild.db` is a 30,000-member sample with 14,782 `mentoring` rows (README.md; counted on the sample).
- Hot path: every forum message resolves its @mentions through `queries/member_by_handle.sql`, about 30 lookups a second at peak, and "Find a mentor" uses it too (README.md, `guild/mentions.py`).
- Rare path: `queries/mentor_line.sql` is shown on a profile (README.md).
- Invariants: handles are unique ignoring case; `guild/signup.py` stores the handle as typed, minus surrounding spaces; each member has at most one recorded mentor; a mentor must have joined before the mentee (README.md, `migrations/001_members.sql`, `migrations/003_mentor_order.sql`).
- Writers and rates: not stated beyond signup and the forum.

## Findings

### high: `member_by_handle.sql`
The migration comment promises "this index also serves handle lookups". The query then asks for `lower(trim(handle))`, which is a different question, and the index declines to answer questions it was not asked.
Problem: When a forum message with @mentions is posted, `resolve_mentions` runs `queries/member_by_handle.sql` once per mention, and the statement filters on `lower(trim(handle))`. The only handle index, `member_handle_ci` in `migrations/002_handle_index.sql`, is on `lower(handle)`; an expression index is used only for the identical expression. `EXPLAIN QUERY PLAN` on `guild.db` says `SCAN member`, and a lookup took about 12 ms on 30,000 rows. At 350,000 members the statement must read about twelve times as many rows whatever the planner does, for every mention, at about 30 lookups a second. The `trim()` buys nothing: `guild/signup.py` strips the handle on the way in, the sample has no padded handle, and `MENTION` in `guild/mentions.py` cannot produce a space.
Fix: `WHERE lower(handle) = lower(:handle);`. I ran `EXPLAIN QUERY PLAN` on it against `guild.db`: `SEARCH member USING INDEX member_handle_ci (<expr>=?)`, about 0.07 ms. No migration; the index exists.

### low: `resolve_mentions`
A message that says @sam six times asks the database about sam six times, which is dedication.
Problem: `resolve_mentions` looks up every match from `MENTION.findall`, including repeats, while `found` keeps one entry per handle. With the index in place a repeat costs well under a millisecond, so this is minor, not the cause of the slowness.
Fix: Iterate the distinct handles, for example `dict.fromkeys(MENTION.findall(text))`, so each is looked up once per message.

## Holds up
- `member_handle_ci` (`CREATE UNIQUE INDEX ... ON member(lower(handle))`): enforces the stated rule that handles are unique ignoring case, and it is the right index for the fixed query. The sample has no two handles that differ only in case. What would change this: non-ASCII handles (SQLite's `lower()` handles ASCII only), but `HANDLE` in `guild/signup.py` allows ASCII letters, digits and `_` only.
- `queries/mentor_line.sql`: `UNION ALL` with no depth guard looks alarming, but a loop cannot exist. `mentoring.mentee_id` is the primary key, so each member has one mentor, and `mentoring_mentor_joined_first` and `mentoring_mentor_joined_first_upd` in `migrations/003_mentor_order.sql` abort any insert or update where the mentor did not join strictly before the mentee, so every step goes to an earlier join date and cannot return. In the sample: 0 loops, 0 rows violating the order, longest line 10 steps. Each step is a primary key search. What would change this: something that changes `member.joined_on` after the link is made (no file does), or writes to `mentoring` with the triggers dropped; an optional depth limit would be insurance only.
- `queries/mentees_of.sql`: uses `mentoring_by_mentor` (`SEARCH g USING INDEX mentoring_by_mentor`), with a small sort by `since` for one mentor's mentees. The index is exactly what it needs.
- `mentoring` primary key and `CHECK (mentee_id <> mentor_id)`: one mentor per member, no self-mentoring, and the sample has no row pointing at a missing member.

## Not checked
- Production: only the 30,000-member sample was run. The 350,000-member cost is extrapolated from the sample plan (a scan reads every row); the index search needs no extrapolation.
- Foreign keys: nothing in the repo turns `PRAGMA foreign_keys` on, and no file writes to `mentoring` apart from the triggers' use in migrations, so I could not see how it is written in production.
- The forum code that calls `resolve_mentions`: not in the repo.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

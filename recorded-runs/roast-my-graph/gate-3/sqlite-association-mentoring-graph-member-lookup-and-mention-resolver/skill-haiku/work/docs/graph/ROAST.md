# Roast: guild (migrations/, queries/, guild/)

Verdict: One query is the slowdown. `queries/member_by_handle.sql` wraps the handle in `trim()` and `lower()`, which the unique index `member_handle_ci` (on `lower(handle)`) cannot serve, so every @mention scans the whole `member` table. Change the predicate to `lower(handle) = lower(:handle)`. That is high severity on the forum path, and the rest is medium or low.

Judged against:
- Members: about 350,000 in production; the `guild.db` sample has 30,000 (`README.md`; counted read-only).
- Hot path: every forum message resolves its @mentions through `queries/member_by_handle.sql`, about 30 lookups a second at peak (`README.md`).
- Profile lineage: `queries/mentor_line.sql` is read on the profile page, not the forum (`README.md`).
- Handles: unique ignoring case; signup stores the handle as typed, minus surrounding spaces (`README.md`, `guild/signup.py`). The sample has no handle with surrounding spaces and no case-duplicates.
- Mentoring: at most one mentor per mentee; the mentor must have joined before the mentee (`migrations/001_members.sql`, `migrations/003_mentor_order.sql`). The sample has 14,782 mentoring rows, none violating the join order, none self-mentored, and no lineage loops (longest chain 10).
- Engine: SQLite (version not stated in the repo; the local SQLite is 3.53.1, as run here).

## Findings

### high: `queries/member_by_handle.sql`
Problem: the predicate `lower(trim(handle)) = lower(trim(:handle))` is not the expression the index holds (`member_handle_ci` on `lower(handle)`), so the planner does `SCAN member` (EXPLAIN QUERY PLAN, run read-only on the sample). On the 30,000-member sample one lookup takes about 4.7 ms (300 lookups in 1.42 s). The sample scales linearly, so at 350,000 members one lookup is roughly 55 ms (an extrapolation, not measured). At about 30 lookups a second that is about 1.6 seconds of work per second, more than one core on the forum's hot path, and every message with several mentions multiplies it.
Fix: `SELECT id, handle, full_name FROM member WHERE lower(handle) = lower(:handle);`. EXPLAIN QUERY PLAN then shows `SEARCH member USING INDEX member_handle_ci (<expr>=?)`, and one lookup took about 0.01 ms on the sample (300 lookups in 0.003 s), returning the same rows for the 300 handles tested. This drops `trim()`, which is safe because no stored handle has surrounding spaces and signup strips them and rejects others by regex. If another writer could store spaces, the index would not catch them either, so that writer needs fixing too. Assumes SQLite 3.53.1; the expression-index match is standard SQLite behaviour.

### medium: `resolve_mentions`
Problem: `guild/mentions.py` runs one lookup for every @mention occurrence (`MENTION.findall(text)`), so a message that names the same member five times runs five lookups for one profile. After the index fix each lookup is cheap, but the repeat is still a real cost on the hot path.
Fix: look up each handle once, for example `for handle in dict.fromkeys(MENTION.findall(text)):`, and keep the dict as it is.

### low: `member` (joined_on)
Problem: the trigger `mentoring_mentor_joined_first_upd` checks join order only when `mentoring` rows change. Nothing in the files updates `member.joined_on` (the only write is the insert in `guild/signup.py`), but if a later change edited `joined_on` after mentoring rows exist, the order could break, and `queries/mentor_line.sql` (which relies on it to stop) could loop. Whether `joined_on` can change is not stated.
Question to confirm: is `joined_on` ever updated? If yes, add a trigger on `member` that rejects the change while a mentoring row depends on it.

## Holds up
- `mentor_line` (`queries/mentor_line.sql`): `UNION ALL` with no depth bound is fine here. Each member has at most one mentor (`mentoring.mentee_id` is the primary key, the rowid alias, so each step is a direct lookup), and the join-order trigger makes each step strictly earlier in time, so a loop cannot form. The sample has no loops and a longest chain of 10. Reverse this if `joined_on` can change (see the low finding above).
- `mentees_of` (`queries/mentees_of.sql`): `mentoring_by_mentor` leads with `mentor_id`, so the lookup is a search; the sort is over one mentor's mentees.
- `mentoring_mentor_joined_first` and `..._upd` triggers (`migrations/003_mentor_order.sql`): they enforce the join order on insert and on changes to `mentor_id` or `mentee_id`, and the sample has no violations.
- `member_handle_ci` (`migrations/002_handle_index.sql`): a unique index on `lower(handle)`, which is the right index for case-insensitive lookups. It is only used once the query matches it (see the high finding).
- `mentoring.mentee_id` primary key: one mentor per mentee, as the README and the migration state.

## Not checked
- The production database and the 350,000-member timing. The 55 ms per lookup is an extrapolation from 30,000 rows.
- The forum's real concurrency and whether the database runs on the same host as the web tier.
- Whether any writer besides `guild/signup.py` stores handles with spaces (none in the sample).
- Whether a message can carry an unlimited number of @mentions; no limit appears in the files.
- The fix was run on the sample only; the production SQLite version was not checked.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

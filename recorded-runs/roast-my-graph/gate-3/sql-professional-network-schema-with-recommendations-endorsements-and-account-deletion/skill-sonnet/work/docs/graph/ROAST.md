# Roast: Linkwell network schema (db/schema.sql, db/queries/)

Verdict: One thing blocks launch. "Delete my account" will not finish inside the 10-second gateway cut, because `recommendation.author_id` has an `ON DELETE CASCADE` foreign key and no index that starts with it, so every deletion reads all 140 million recommendations. One index fixes it. Everything else is medium or low or sound.

Judged against:
- Engine: PostgreSQL 16 (README.md, db/schema.sql). Plans below were run on a local PostgreSQL 16 with scaled-down sample data I generated, so they show plan shape, not production speed.
- Sizes: account 9.1 million, follows 412 million, endorsement 305 million, recommendation 140 million (body is free text, 1.2 KB on average), block 6 million, skill 38 thousand (README.md).
- Interactive: profile pages show followers, following, endorsements received grouped by skill, and recommendations about the member (README.md).
- Delete my account: runs `delete_account.sql` inside the request, the gateway cuts requests at 10 seconds, about 20 thousand deletions a day and more after news stories, everything the member created goes through `ON DELETE CASCADE` (README.md).
- Skills: never deleted or renamed, retired with `retired_at`; the API loads the active list once at start-up (README.md).
- Endorsement counts per skill come from the analytics warehouse; Postgres never answers them (README.md).
- Maximum followers per account: not stated.

## Findings

### critical: `recommendation`
A table of 140 million 1.2 KB essays, and the account-deletion button wants to read every one of them, 20 thousand times a day.
Problem: when `delete_account.sql` runs, `recommendation_author_id_fkey` (`author_id ... ON DELETE CASCADE`) has to find the member's authored rows. Only `recommendation_pkey` and `recommendation_subject (subject_id, written_at DESC)` exist, and neither starts with `author_id`, so every deletion reads the whole table (about 170 GB of heap at 140 million rows of 1.2 KB). I ran `EXPLAIN ANALYZE DELETE FROM account WHERE id = 5` on a 1 million row sample: the author trigger took 195 ms against 1 to 2 ms for the other seven constraints; with `recommendation_author` it dropped to 0.2 ms. Scaled to 140 million rows the scan alone is far beyond the 10-second gateway cut, on the main path, every day. The other seven foreign keys on `account` all have a leading index (checked below).
Fix: `CREATE INDEX CONCURRENTLY recommendation_author ON recommendation (author_id);` (PostgreSQL 16; CONCURRENTLY cannot run inside a transaction block, and the build on 140 million rows takes a while, so schedule it). Re-run `EXPLAIN (ANALYZE) DELETE FROM account WHERE id = <id>` on a staging copy and confirm the author trigger is an index search. Accounts with very large follows or endorsements may still be slow; measure the biggest account before launch.

### medium: `followers.sql`
Problem: `WHERE f.followee_id = $1 ORDER BY f.since DESC LIMIT 50` uses `follows_followee (followee_id, follower_id)`, which does not contain `since`, so the statement reads every follower of the profile and then keeps the newest 50. I confirmed the plan on a sample account with 100,000 followers: it reads all 99,999 rows, joins them to `account`, and only then sorts for the top 50 (133 ms). The cost grows with followers on every profile view. The files do not state the largest follower count (the README average is about 45 per account), so this is medium: it becomes high if accounts with millions of followers exist.
Fix: `CREATE INDEX CONCURRENTLY follows_followee_since ON follows (followee_id, since DESC, follower_id);` then drop `follows_followee`, which it replaces for the cascade lookup on `followee_id` as well. Then the query reads 50 index entries.

### low: `following.sql`
Problem: the same shape as `followers.sql`: `WHERE f.follower_id = $1 ORDER BY f.since DESC LIMIT 50` finds rows through the primary key `(follower_id, followee_id)`, which does not hold `since`, so it reads every account the member follows and sorts. Nothing in the files states a cap on how many accounts a member follows; if they follow tens of thousands, this becomes medium. Question to confirm: is there a follow limit?
Fix: if confirmed needed, `CREATE INDEX CONCURRENTLY follows_follower_since ON follows (follower_id, since DESC, followee_id);`. The primary key already covers the cascade lookup on `follower_id`, so nothing else changes.

## Holds up
- `follows`, `endorsement`, `block` and the `recommendation.subject_id` key: every cascade key on `account` has an index that starts with it (`follows` primary key and `follows_followee`; `endorsement` primary key and `endorsement_received`; `block` primary key and `block_blocked`; `recommendation_subject`). The trigger times in the sample delete confirm this. `block_blocked (blocked_id)` is not redundant: the primary key cannot serve `blocked_id` lookups.
- `endorsement.skill_id` (no index on the key to `skill`): skills are never deleted or renamed (README.md), so nothing ever has to find endorsements by skill for a delete. What would change that: a skill ever being deleted.
- `endorsements_for_profile.sql`: `endorsement_received (receiver_id, skill_id)` holds both columns the query needs, so it reads one member's entries from the index and groups them. The platform-wide counts per skill come from the warehouse, so there is no whole-table `count(*)` on Postgres.
- `recommendations_for_profile.sql`: `recommendation_subject (subject_id, written_at DESC)` returns the newest 10 in order and stops; the `account` join is ten primary-key lookups.
- `is_blocked.sql`: a point lookup on the primary key `(blocker_id, blocked_id)`.
- `active_skills.sql`: 38 thousand rows, loaded once at start-up and cached; no index needed.
- `account.handle` and `skill.name` `UNIQUE`: the lookups by them are served by the index the constraint creates.

## Not checked
- Production speed: the plans were run on scaled-down generated data on a local PostgreSQL 16, so only plan shape and trigger timings were compared, not the 10-second budget itself.
- The largest follower or following count, the largest account's cascade size, and how long the index builds will take on production.
- How the API resolves skill names for retired skills on a profile (`endorsements_for_profile.sql` returns `skill_id`; the in-memory list holds active skills only; the API is not in the repo).

Roasted with erdostack: npx skills add usergraphtheory/erdostack

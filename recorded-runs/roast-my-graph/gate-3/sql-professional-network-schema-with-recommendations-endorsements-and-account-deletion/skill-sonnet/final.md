One launch blocker, and it is a single index.

**Critical: "Delete my account" will not finish in 10 seconds.** `recommendation.author_id` has `ON DELETE CASCADE`, but neither `recommendation_pkey` nor `recommendation_subject (subject_id, written_at DESC)` starts with `author_id`. So every deletion reads all 140 million recommendations (about 170 GB at 1.2 KB each), about 20 thousand times a day. I ran `EXPLAIN ANALYZE DELETE FROM account` on PostgreSQL 16 with a 1 million row sample: the author trigger took 195 ms against 1 to 2 ms for the other seven constraints. After adding the index it took 0.2 ms. Fix: `CREATE INDEX CONCURRENTLY recommendation_author ON recommendation (author_id);`. It cannot run in a transaction block and the build is long, so schedule it.

Everything else:
- Medium, `followers.sql`: the index lacks `since`, so a profile reads every follower before keeping the newest 50. The largest follower count isn't stated, so it is medium (high if accounts with millions of followers exist). Fix: `follows_followee_since (followee_id, since DESC, follower_id)`, replacing `follows_followee`.
- Low, `following.sql`: the same shape, and only a question: is there a cap on how many accounts a member follows?
- Sound: the other seven cascade keys, `endorsements_for_profile.sql`, `recommendations_for_profile.sql`, `is_blocked.sql` and `active_skills.sql`. `endorsement.skill_id` needs no index because skills are never deleted.

Not checked: production speed (I used scaled-down data I generated, so these are plan shapes, not the 10-second budget), the largest accounts' cascade size, and how the API names retired skills on a profile.

Files: findings.json in the repo root, and docs/graph/ROAST.md.

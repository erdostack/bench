Summary for the launch review: one critical blocker, two high problems, a few smaller ones. The schema is otherwise tidy. I read the SQL and the README sizes and did not run it, because there is no Postgres server on this machine, so the estimates below come from the row counts, not from query plans.

**Blocker**
- `recommendation.author_id` has an `ON DELETE CASCADE` foreign key but no index starting with `author_id`. Every other cascading column on `follows`, `endorsement` and `block` is covered by the primary key or an index. So every `delete_account.sql` has to scan the whole 140 million row `recommendation` table (about 1.2 KB of text per row) to find that member's recommendations. That takes minutes against a 10 second gateway limit, at about 20 thousand deletes a day. Fix: `CREATE INDEX CONCURRENTLY recommendation_author ON recommendation (author_id);` before launch.

**High**
- `delete_account.sql` runs inside the request and cascades through everything in one transaction. Even with the index, a member with millions of followers or endorsements will blow the 10 second limit, and deletions go up after news stories. Soft-delete the account (`deleted_at`) and hide it at once, then remove dependent rows in batches in a background job, with the cascade only as a safety net.
- `followers.sql` is `ORDER BY since DESC LIMIT 50`, but `follows_followee` is on `(followee_id, follower_id)`, with no `since`. Postgres reads and sorts every follower of the member to return 50. That is millions of rows for a popular profile, on every view. Replace the index with `(followee_id, since DESC, follower_id)`. It still serves the cascade lookup.

**Medium and low**
- `following.sql` has the same sort problem through the primary key, but it is bounded by how many accounts a member follows. Add `(follower_id, since DESC, followee_id)` only if those counts are large.
- `account.handle` is `UNIQUE` and case-sensitive, so `Ada` and `ada` can both exist. Use a unique index on `lower(handle)`.
- There are no checks against self-endorsement, self-follow, self-block or self-recommendation.
- `active_skills.sql` is loaded once at start-up, so a skill retired later keeps being offered until the process restarts.

Not a problem: `endorsements_for_profile.sql` is covered by `endorsement_received` (the global per-skill counts come from the warehouse, as the README says), `recommendations_for_profile.sql` uses `recommendation_subject` well, and `is_blocked.sql` hits the primary key.

`findings.json` in the repo root has eight entries in the format you asked for.

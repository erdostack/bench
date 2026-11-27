# Roast: Linkwell network schema (db/)

Verdict: Not sound for the launch review. The account delete path cannot finish at the stated size, because recommendation.author_id has no index and the cascade scans about 140 million rows inside a 10-second request. The same path also deletes content other members wrote about the deleted account.

Judged against:
- PostgreSQL 16 (db/schema.sql header; README.md)
- Production sizes, November 2026: account 9.1 million, follows 412 million, endorsement 305 million, recommendation 140 million (1.2 KB body on average), block 6 million, skill 38 thousand (README.md)
- Delete my account runs delete_account.sql inside the request; the API gateway cuts requests at 10 seconds; about 20 thousand accounts a day, more after news stories (README.md)
- "Everything the member created goes with the account, through the ON DELETE CASCADE keys" (README.md)
- Skills are never deleted; active_skills.sql loads them once at start-up (README.md)
- Endorsement counts per skill come from the analytics warehouse, not Postgres (README.md)

## Findings

### critical: `recommendation`
The rant: the table has an index for everything except the one column the delete path needs, which is a fine way to ensure the delete is the slowest query in the building.
Problem: recommendation.author_id REFERENCES account ON DELETE CASCADE, and the table's only index leads with subject_id. PostgreSQL does not index referencing columns, so each account delete runs the cascade as a sequential scan of about 140 million rows at 1.2 KB of body each. delete_account.sql runs inside the request, the gateway cuts it at 10 seconds, and about 20 thousand deletes run each day. The cascade cannot finish in that window at the stated size.
Fix: CREATE INDEX CONCURRENTLY recommendation_author ON recommendation (author_id); (PostgreSQL 16). Then move the deletion off the request path: mark the account deleted in the request, and let a background job delete the rows in batches. Check the plan with EXPLAIN (ANALYZE, BUFFERS) on a staging copy before and after.

### high: `recommendation`
The rant: the README says the member's own things leave with them, and the cascade on subject_id also takes the things other people wrote about the member, which is a surprise to everyone except the cascade.
Problem: recommendation.subject_id REFERENCES account ON DELETE CASCADE. A recommendation written by someone else about the deleted member is removed, against the README's rule that the cascades remove what the member created. Trigger: any member who has received a recommendation, which the 140 million rows make routine.
Fix: Product decision. If these recommendations must survive, make subject_id nullable with ON DELETE SET NULL, and hide them in recommendations_for_profile.sql. If they must go, say so in the README. Confirm with the owner before the launch review.

### high: `endorsement`
The rant: an endorsement that Ada gave Grace is Ada's, and it disappears when Grace leaves, which the README's wording does not appear to intend.
Problem: endorsement.receiver_id REFERENCES account ON DELETE CASCADE. The endorsement was created by giver_id, not by the deleted member, so the README's rule does not cover its removal. Trigger: any member who has received an endorsement, which the 305 million rows make routine. The change stream also carries these deletions into the analytics warehouse.
Fix: Decide with the product owner. If the endorsement should survive, make receiver_id nullable with ON DELETE SET NULL, and filter those rows in endorsements_for_profile.sql. If it should not, keep the cascade and document it.

### medium: `follows`
The rant: the index was built for "who follows me", and then the query asked for "who followed me most recently", which the index cannot answer.
Problem: followers.sql filters on followee_id and sorts by since DESC with LIMIT 50. The only index is follows_followee (followee_id, follower_id), which does not include since. Postgres reads every follower of the account and fetches each heap tuple to sort it, then keeps 50. The shipped data is not known to hold an account with millions of followers, so this is a medium.
Fix: CREATE INDEX CONCURRENTLY follows_followee_since ON follows (followee_id, since DESC) INCLUDE (follower_id); (PostgreSQL 11 or later), so the first 50 come off the index in order.

### low: `following.sql`
The rant: the same sort problem as followers, at a smaller scale, which is still a sort.
Problem: following.sql filters on follower_id and sorts by since DESC. The primary key (follower_id, followee_id) does not include since, so Postgres sorts every row for the member. The cost is bounded by how many accounts one member follows, which the README does not give.
Fix: CREATE INDEX CONCURRENTLY follows_follower_since ON follows (follower_id, since DESC) INCLUDE (followee_id); Skip it if no member follows more than a few thousand accounts.

### low: `block_blocked`
The rant: an index that nothing in the repo uses, on a table that is small enough to forgive, though not forever.
Problem: block_blocked on block (blocked_id) is not used by any statement in db/queries/. The API is not in this repo, so it may use it. is_blocked.sql also checks one direction only, so a block does not stop the blocked member seeing the blocker unless the API checks both ways.
Fix: Check the API for lookups by blocked_id. If there are none, drop block_blocked. Confirm with product whether blocks are symmetric, and if they are, check both directions in is_blocked.sql.

## Holds up
- `active_skills.sql`: one read at start-up, over a 38 thousand row table. Skills are never deleted, so the skill_id foreign keys have no cascade to index.
- `endorsements_for_profile.sql`: served by endorsement_received (receiver_id, skill_id), so the count per skill comes from an index-only read. It gets slower for profiles with very many endorsements, which the README does not size.
- `recommendations_for_profile.sql`: served by recommendation_subject (subject_id, written_at DESC), so the top 10 come straight off the index.
- `is_blocked.sql`: served by the primary key (blocker_id, blocked_id).
- Cascade keys on follows (follower_id via the primary key, followee_id via follows_followee), endorsement giver_id (primary key), block blocker_id (primary key) and blocked_id (block_blocked): each is covered by an index.

## Not checked
- psql is installed, but there is no PostgreSQL server, so no plan was run.
- The API is not in this repo, so I could not see how it calls the queries, or whether it reads block by blocked_id.
- The size of the largest accounts is not in the README, so the follows findings are sized from the averages only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

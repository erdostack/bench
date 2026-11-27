Added jobs/backfill_depth.py. It works out every post's depth first, walking down from the first posts
of each thread with a recursive query into a temp table, and then writes the depths in chunks of 2,000
with a commit after each chunk.

I did not do it in id order: merged threads (docs/moderation.md) hang the moved first post under a newer
post in another thread, and 420 first posts point at a higher id, so a parent-before-child pass by id
would leave those threads NULL. On a copy of var/threadline.db it fills all 60,000 posts (max depth 39)
and returns 60,000.

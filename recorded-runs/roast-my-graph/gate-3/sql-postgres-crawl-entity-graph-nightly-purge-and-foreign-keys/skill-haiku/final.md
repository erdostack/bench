The nightly purge cannot finish between 01:00 and 03:00 at this size, and its single transaction can hold up crawl writers that touch the entities it is deleting. Two changes, in this order.

1. Add an index on `relation (dst)`. The only key on `relation` leads with `src`, so every deleted entity makes the `dst` cascade scan up to 220 million rows. Build it with `CREATE INDEX CONCURRENTLY relation_dst ON relation (dst);` before the next run. Check `EXPLAIN DELETE FROM relation WHERE dst = $1;` on a copy first.
2. Split `jobs/purge_stale.sql` into batches of about 5,000 entities, one transaction each, with `FOR UPDATE SKIP LOCKED` so a batch never waits on a writer. Repeat the age test in the outer `DELETE`. A single transaction holds locks on all 300,000 entities until it commits, so any writer that touches one of them waits for the whole purge. The files do not show how often that happens.

What holds up: the `entity_last_seen` index serves the purge's selection, the primary key serves the cascade on `src` and the outward walk in `queries/out_neighbours.sql`, and `queries/upsert_relation.sql` uses the key as its conflict target.

Not run. There is no PostgreSQL server on this machine. The index finding rests on the rule that a foreign key does not create an index on the referencing column, which the skill's notes mark as unverified, so confirm it on a copy first. Check that the production database does not already have a `relation (dst)` index. The review is in `docs/graph/ROAST.md` and the findings in `findings.json`, both under `/run/work`.

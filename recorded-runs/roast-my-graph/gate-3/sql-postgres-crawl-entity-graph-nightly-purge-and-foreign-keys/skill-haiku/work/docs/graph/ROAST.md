# Roast: kg (schema.sql, jobs/, queries/)

Verdict: Not sound for the nightly purge. `relation` has no index that leads with `dst`, so when `jobs/purge_stale.sql` deletes an entity, the cascade on the `dst` foreign key has to scan the relation table. The purge deletes about 300,000 entities a night against 220 million relations, so it cannot finish between 01:00 and 03:00. Its single transaction also holds locks until it ends, which can stall any crawl writer that touches a purged entity. Fix the index first, then split the purge into batches.

Judged against:
- PostgreSQL 16, image `postgres:16.4` (`README.md`; `docker-compose.yml`).
- The purge runs nightly at 01:00 and must finish by 03:00, when the crawl writers start. It deletes entities not seen for 90 days, about 300,000 a night. Their relations, in either direction, go with them through `ON DELETE CASCADE` (`README.md`; `jobs/purge_stale.sql`).
- Sizes: 60 million entities, 220 million relations (`README.md`).
- The app walks relations outward from an entity only (`README.md`; `queries/out_neighbours.sql`).
- `entity_kind` is a fixed list of 12 kinds, seeded once and never changed (`README.md`; `schema.sql`). `queries/kind_counts.sql` feeds a weekly dashboard (`README.md`).

## Findings

### critical: `relation`
Problem: `relation` has `dst bigint NOT NULL REFERENCES entity(id) ON DELETE CASCADE` and a primary key `(src, rel, dst)`. That key leads with `src`, so nothing in `schema.sql` leads with `dst`. When `jobs/purge_stale.sql` deletes one of the roughly 300,000 entities a night, the cascade on `dst` must find the relations pointing at it, and with no index that is a sequential scan of up to 220 million rows, once per deleted entity. The job cannot finish by 03:00 at this size.
Fix: `CREATE INDEX CONCURRENTLY relation_dst ON relation (dst);`, run outside a transaction and before the next purge. Building it on 220 million rows will take a long time, and it adds write cost to the crawl writers. Check the plan on a copy first: `EXPLAIN DELETE FROM relation WHERE dst = $1;` should show an index scan on `relation_dst`. Assumes PostgreSQL 16.4 from `docker-compose.yml`.

### medium: `jobs/purge_stale.sql`
Problem: The job is one `DELETE FROM entity WHERE last_seen < now() - interval '90 days';`, so one transaction holds row locks on the whole batch of about 300,000 entities and on their cascaded relations until it commits. A crawl writer inserting a relation takes a key-share lock on each entity it references (through the foreign key), and those locks conflict with the purge's row locks. So a writer that touches a purged entity waits for the whole purge. The files do not show how often that happens; the pile-up the user reports is consistent with it but is not evidence from the files.
Fix: Run the purge in batches, one transaction per batch, with a cutoff computed once when the job starts. Repeat the age test in the outer `DELETE` so an entity re-seen after the batch was selected is kept:
```sql
DELETE FROM entity
WHERE id IN (
  SELECT id FROM entity
  WHERE last_seen < :cutoff
  LIMIT 5000
  FOR UPDATE SKIP LOCKED
)
AND last_seen < :cutoff;
```
Repeat until a batch deletes zero rows. `SKIP LOCKED` leaves rows a writer holds for a later batch, so a batch never waits on a writer. Confirm the syntax on PostgreSQL 16.4 before deploying; this has not been run.

## Holds up
- `entity_last_seen (last_seen)`: the purge's age test is a range search on this index, so it does not scan the 60 million entities.
- `relation` primary key `(src, rel, dst)`: the cascade on `src` is served by this key, since it leads with `src`. `queries/out_neighbours.sql` filters on `r.src = $1` and uses the same key.
- `queries/out_neighbours.sql`: the `ORDER BY r.rel, e.label` sorts only one entity's outgoing relations. At the stated size of 220 million relations over 60 million entities, that is about 3.7 per entity on average. The out-degree of hub entities is not stated, so the sort's worst case is not known. The index serves the search; the sort is small at that average.
- `queries/upsert_relation.sql`: `ON CONFLICT (src, rel, dst)` matches the primary key exactly, so each upsert uses the key as its conflict target.
- `queries/kind_counts.sql`: scans `entity` for a weekly dashboard with no index on `kind_id`. The dashboard is a batch job, so the scan is acceptable.
- `entity_kind`: 12 fixed rows, `name` unique, and nothing deletes or updates them, so the foreign key from `entity.kind_id` needs no cascade.

## Not checked
- No PostgreSQL server is on this machine. `psql` is present, but there is no `postgres` binary and no data directory. Nothing was run.
- The `critical` finding rests on the rule that a foreign key does not create an index on its referencing column, and that a cascade scans for the child rows. `references/engines.md` marks this as unverified, and the official docs were not read here. Before the index is built, confirm it with `EXPLAIN` on a copy of the database.
- The production database may differ from `schema.sql`. If an index on `relation (dst)` already exists there, the finding is wrong. Check with `\d relation`.
- The purge's runtime, lock waits and the size of `CREATE INDEX CONCURRENTLY` were not measured.
- The batch loop is a sketch. The job runner that calls it is not in the repo.
- `docker-compose.yml` is outside the scope of this review, apart from the image version.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

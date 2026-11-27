# Roast: kg (schema.sql, jobs/, queries/)

Verdict: the nightly purge overruns because `relation` has no index on `dst`: every deleted entity makes PostgreSQL scan 220 million relations to find the ones pointing at it. One index fixes it. Critical; the rest is sound.

Judged against: PostgreSQL 16 (`postgres:16.4` in docker-compose.yml); 60 million entities and 220 million relations (README.md); `jobs/purge_stale.sql` runs at 01:00, must finish by 03:00 when the crawl writers start, deletes about 300,000 entities a night, relations in either direction removed through `ON DELETE CASCADE` (README.md); the app only walks relations outward, `queries/out_neighbours.sql` (README.md); `entity_kind` is 12 fixed rows, `kind_counts.sql` feeds a weekly dashboard (README.md).

## Findings

### critical: `dst`
The cascade goes looking for everyone who ever pointed at a deleted entity, in a table of 220 million rows, with no index, 300,000 times. The planner is not slow; it is being asked to read the whole phone book to find the callers.
Problem: When `purge_stale.sql` deletes about 300,000 entities, `ON DELETE CASCADE` on `relation.dst` must find the rows with `dst = <deleted id>`; no index leads with `dst` (the primary key `(src, rel, dst)` serves `src` only, and PostgreSQL does not index a foreign key's referencing column), so each one is a scan of 220 million rows. The job cannot finish by 03:00.
Fix: `CREATE INDEX CONCURRENTLY relation_by_dst ON relation (dst);` (PostgreSQL 16.4; run outside a transaction; the live database needs it run by hand because `schema.sql` only runs at creation) and add `CREATE INDEX relation_by_dst ON relation (dst);` to `schema.sql`. Confirm with `EXPLAIN (ANALYZE)` that the cascade uses it.

### low: `purge_stale.sql`
Problem: one statement and one transaction for about 300,000 entities and their relations holds locks and WAL until it ends. Fine once the index exists; hardening only.
Fix: optional batching of 10,000 ids per transaction using `entity_last_seen`.

## Holds up
- `entity_last_seen`: serves the purge predicate `last_seen < now() - interval '90 days'`.
- `relation` primary key `(src, rel, dst)`: serves `out_neighbours.sql` (`WHERE r.src = $1`) and is the conflict target for `upsert_relation.sql` (`ON CONFLICT (src, rel, dst)`). The `ORDER BY r.rel, e.label LIMIT 200` sorts one entity's neighbours, bounded by the entity's out-degree.
- `kind_counts.sql`: reads every entity once, by design for a weekly dashboard; `entity.kind_id` needs no index for it. `entity_kind` is 12 fixed rows, so the foreign key from `entity.kind_id` never cascades.

## Not checked
- Nothing was run: `psql` is installed here but no server with the 60 million rows; the missing-index cost is derived from the DDL and the sizes in the README, and the PostgreSQL foreign-key behaviour is from `engines.md` (marked unverified there). Whether `relation` has other indexes in the live database that `schema.sql` does not show was not checked.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

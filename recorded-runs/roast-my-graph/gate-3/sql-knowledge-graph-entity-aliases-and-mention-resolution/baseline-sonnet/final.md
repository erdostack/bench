**Likely cause of the ingest slowdown:** the 2026-10-14 change to `queries/resolve_mention.sql`.

That change made the filter `lower(trim(alias_text)) = lower(trim($1))`. The only matching index, `alias_norm`, is on `lower(alias_text)`. PostgreSQL uses an expression index only when the query has exactly the indexed expression, so this filter no longer has an index. As I read it, every mention lookup scans the 31 million row alias table, at about 50 thousand mentions a minute. That fits "falling behind since last month".

I couldn't run PostgreSQL here, so this comes from reading `schema.sql` and the queries. Confirm it with `EXPLAIN (ANALYZE, BUFFERS)` on a real alias.

**Fix, in order:**
1. `CREATE INDEX CONCURRENTLY alias_norm_trim ON alias (lower(trim(alias_text)));`, then `ANALYZE alias` and check the plan.
2. `DROP INDEX CONCURRENTLY alias_norm;` once the plan is confirmed. Nothing uses it now, but it still slows every alias write.
3. Clean the old trailing-space aliases once and normalise on write, so queries don't have to repeat the trim.

**Other findings:**
- **resolve_mention ranking:** it ranks by `count(*)` of alias rows. `alias` has no unique constraint and `add_alias.sql` is a plain `INSERT`, so duplicated rows inflate the count and the wrong entity can win. Ties have no deterministic order.
- **add_alias:** add a unique index on (entity_id, lower(trim(alias_text)), source) and use `ON CONFLICT DO NOTHING`.
- **relation_by_dst:** it lacks `src_id`, which `incoming.sql` needs for its join. Recreate it as `(dst_id, predicate) INCLUDE (src_id)` so it can be an index-only scan.
- **incoming.sql and outgoing.sql:** both are unbounded with no tie-breaker on `ORDER BY predicate`. A hub entity can return hundreds of thousands of rows. Use keyset pagination.
- **entity_aliases.sql:** an index on (entity_id, alias_text) would remove the sort.
- **Schema:** `kind` and `predicate` are free text, and there is no provenance or created-at on `alias` or `relation`.

All 10 findings, with severity and fixes, are in findings.json at the repo root, ready to paste. I didn't change any code.

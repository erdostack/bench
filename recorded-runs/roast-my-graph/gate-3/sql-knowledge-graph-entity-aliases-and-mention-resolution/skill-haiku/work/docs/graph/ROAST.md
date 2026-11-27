# Review: kg-store schema and queries (PostgreSQL 16)

Verdict: Not sound as it stands. The slowdown is a critical problem: the 2026-10-14 change added `trim()` to `queries/resolve_mention.sql`, so the query no longer matches the `alias_norm` index, and each mention scans the whole alias table. The fix is to remove the stored padding once and then query the index-friendly form. The rest of the schema and the other queries are sound.

Judged against:
- PostgreSQL 16 (`README.md`).
- Sizes: 9 million entities, 31 million aliases, 120 million relations (`README.md`).
- Ingest resolves about 50,000 mentions a minute with `queries/resolve_mention.sql` (`README.md`).
- The entity page shows aliases and relations in both directions (`README.md`).
- 2026-10-14: trim added to both sides of the alias match, because some aliases from the 2025 bulk import have trailing spaces. 2026-06-02: `alias_norm` index for case-insensitive lookup. 2026-03-20: `relation_by_dst` for incoming relations (`CHANGELOG.md`).

## Findings

### critical: `queries/resolve_mention.sql`
Problem: The WHERE clause compares `lower(trim(alias_text))`, but the index on the data is `alias_norm`, on `lower(alias_text)`. PostgreSQL uses an expression index only when the query uses the same expression, so the index is unused and every mention scans the whole alias table. The 2026-10-14 changelog entry added the `trim()` and is the likely start of the ingest backlog. On a two-million-row copy with synthetic data, the statement as written ran a parallel sequential scan (about 256 ms). With an index on `lower(trim(alias_text))`, it ran as an index scan (about 0.07 ms). At 50,000 mentions a minute, a full-table scan per mention cannot keep up. The 31-million-row figure is an extrapolation from the copy, not a measurement.
Fix: Remove the stored whitespace once, then use the index-friendly query. Migration: `UPDATE alias SET alias_text = btrim(alias_text) WHERE alias_text <> btrim(alias_text);`, run in batches and followed by `VACUUM ANALYZE alias;`. Write path: in `queries/add_alias.sql`, use `VALUES ($1, btrim($2), $3)`, and check every other loader that writes alias rows. Query: write `lower(alias_text) = lower(trim($1))` so `alias_norm` is used. Stopgap, if the data cannot be cleaned yet: `CREATE INDEX CONCURRENTLY alias_norm_trim ON alias (lower(trim(alias_text)));`. This matches the current query without changing the data.

### low: `alias`
Problem: Question to confirm. `alias` has no uniqueness on (entity_id, alias_text, source), and `queries/add_alias.sql` inserts without checking. `queries/resolve_mention.sql` ranks entities by `count(*)` over alias rows, so a repeated insert of the same alias raises that entity's score. The files do not say whether `seen` is meant to count occurrences or distinct sources.
Fix: Confirm the intended meaning of `seen`. If it should count distinct sources, use `count(DISTINCT source)` in `queries/resolve_mention.sql`. If an alias should never be stored twice, add a unique constraint on (entity_id, alias_text, source) and use `INSERT ... ON CONFLICT DO NOTHING` in `queries/add_alias.sql`.

## Holds up
- `relation` primary key (src_id, predicate, dst_id): leads with `src_id`, so `queries/outgoing.sql` (filters on `src_id`) is covered.
- `relation_by_dst` on (dst_id, predicate): leads with `dst_id`, so `queries/incoming.sql` is covered.
- `alias_entity` on `alias (entity_id)`: serves `queries/entity_aliases.sql`, and it also covers the `ON DELETE CASCADE` from `entity`.
- Foreign keys from `relation` to `entity` are covered by the indexes above, so cascading deletes do not scan `relation`.

## Not checked
- The 31-million-row cost was extrapolated from a two-million-row copy with synthetic data, not measured on production data.
- The number of padded alias rows in production, and the time the batched cleanup takes, are not in the repo.
- The ingest workers and the 2025 bulk-import loader are not in the repo, so any other code that writes alias rows could not be checked.
- `CREATE INDEX CONCURRENTLY` and the batched update were not timed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

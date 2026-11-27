# Roast: kg-store schema.sql and queries/ (PostgreSQL 16)

Verdict: there is one serious problem and it explains the ingest lag. The 2026-10-14 change to `queries/resolve_mention.sql` wrapped the column in `trim()`, and the only index on that column, `alias_norm`, is on `lower(alias_text)` without the trim, so the query can no longer use it. Every mention now has to read the whole 31-million-row `alias` table. The rest of the schema and queries is sound, apart from two low notes.

Judged against:
- Engine: PostgreSQL 16 (README.md).
- Sizes: entity 9 million, alias 31 million, relation 120 million (README.md).
- Hot path: ingest workers resolve every mention with `queries/resolve_mention.sql`, about 50 thousand mentions a minute, so about 830 a second (README.md).
- Other reads: the entity page shows aliases and relations in both directions (README.md): `entity_aliases.sql`, `outgoing.sql`, `incoming.sql`.
- History: `alias_norm` was added 2026-06-02 for case-insensitive alias lookup; `relation_by_dst` 2026-03-20; on 2026-10-14 `resolve_mention` started trimming both sides because some aliases from the 2025 bulk import have trailing spaces (CHANGELOG.md). The user says ingest has been falling behind since last month.

## Findings

### critical: `resolve_mention.sql`
Somebody fixed a data problem by wrapping the column in a function, which is the database equivalent of fixing a squeaky door by selling the house. The index that took four months to add now sits there on `lower(alias_text)`, perfectly healthy, politely ignored, like a lighthouse on a lake nobody sails.
Problem: `WHERE lower(trim(alias_text)) = lower(trim($1))` has no index that matches that expression: `alias_norm` is `ON alias (lower(alias_text))` (`schema.sql`), and PostgreSQL uses an expression index only for the exact expression. Since the 2026-10-14 change, each of the roughly 50,000 mentions a minute reads all 31 million `alias` rows, whatever the planner does. That fits ingest falling behind since last month. The change before it matched the index: `lower(alias_text) = lower(trim($1))` would have been an index search. I ran the equivalent on SQLite 3.53.1 (not PostgreSQL, which is not installed here): the old form is a SEARCH using the index and the new form is a SCAN of the table; the same rule holds in PostgreSQL.
Fix: make the index match the query (valid in PostgreSQL 16, not run here; it builds on 31 million rows, so use CONCURRENTLY so writes keep flowing):
```
CREATE INDEX CONCURRENTLY alias_norm_trim ON alias (lower(trim(alias_text)));
DROP INDEX CONCURRENTLY alias_norm;
```
Then remove the reason for the trim, so the stored data is clean: have `add_alias.sql` insert `trim($2)`, fix the existing rows in batches (`UPDATE alias SET alias_text = trim(alias_text) WHERE alias_text <> trim(alias_text)`, mind that the trim can collide with rows that already exist, see the low finding below), and then the query can go back to `lower(alias_text) = lower(trim($1))` against `alias_norm`. Check the plan after with `EXPLAIN` (an Index Scan or Bitmap Index Scan on the new index, not a Seq Scan).

### low: `alias_norm`
Problem: since the 2026-10-14 change no query in `queries/` filters on `lower(alias_text)` alone, so `alias_norm` is maintained on every `add_alias.sql` insert into a 31-million-row table and serves nothing.
Fix: drop it when the replacement index above exists (`DROP INDEX CONCURRENTLY alias_norm;`); or keep it and revert the query to the form it serves, if you clean the data first.

### low: `add_alias.sql`
Problem (a question to confirm): `alias` has no uniqueness on `(entity_id, alias_text)` and the insert has no conflict handling, so the same surface form can be stored many times for an entity. `resolve_mention.sql` ranks entities by `count(*)` (named `seen`) and takes the top 5, so repeated rows count as extra votes, and ties between entities have no tie-break. The README describes aliases as each surface form seen, which reads as a set, but nothing in the files shows duplicates exist.
Fix: confirm whether `seen` is meant to count sightings or distinct sources. If it is a set, add a unique index on `(entity_id, lower(trim(alias_text)))` after removing existing duplicates, and use `ON CONFLICT DO NOTHING` in the insert; in either case add a tie-break to the ranking (`ORDER BY seen DESC, entity_id`).

## Holds up
- `alias_entity`, `relation` primary key `(src_id, predicate, dst_id)` and `relation_by_dst (dst_id, predicate)`: every foreign key column has an index leading with it, so the `ON DELETE CASCADE` deletes from `entity` can find their child rows, and `entity_aliases.sql`, `outgoing.sql` and `incoming.sql` are searches by `entity_id`, `src_id` and `dst_id`. `outgoing.sql` and `incoming.sql` also come back already ordered by `predicate`. What would change that: an entity with millions of relations (a hub), which the files do not show.
- `relation` as a table: it joins exactly two entities with a predicate and nothing else refers to it, so it is the relationship it should be (the key is the triple).
- `entity_aliases.sql` ordering by `alias_text`: it sorts one entity's aliases, which is a handful of rows (31 million over 9 million entities, about 3 each).
- `outgoing.sql` / `incoming.sql` join to `entity` by its primary key; fine.

## Not checked
- Nothing was run on PostgreSQL (not installed here); the table and index sizes, plans and the effect of the fix come from the README and the SQL, plus a SQLite check of the expression-index rule.
- Whether the data has duplicate aliases or trailing spaces beyond what the CHANGELOG says; there is no data in the repo.
- How ingest calls `resolve_mention.sql` (batching, connection pool) and how the queue is measured.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

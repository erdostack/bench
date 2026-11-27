The 2026-10-14 trim change to `resolve_mention.sql` is almost certainly why ingest is behind. It's the one serious problem in the schema and queries.

**Critical, `resolve_mention.sql`:** the query now filters on `lower(trim(alias_text))`, but the only index on that column, `alias_norm`, is on `lower(alias_text)`. PostgreSQL only uses an expression index for the exact same expression. So at about 50,000 mentions a minute, each lookup reads all 31 million `alias` rows. Before the change, the query matched the index. I checked that rule with SQLite, since PostgreSQL isn't installed here. The old form is an index search and the new form is a full scan.

The fix is to create the matching index without blocking writes, then drop the old one:
```
CREATE INDEX CONCURRENTLY alias_norm_trim ON alias (lower(trim(alias_text)));
DROP INDEX CONCURRENTLY alias_norm;
```
The trim is only there because some aliases from the 2025 bulk import have trailing spaces. The lasting fix is to trim in `add_alias.sql`, clean the existing rows in batches, and put the query back to its old form. The roast has the details. Check with `EXPLAIN` that the plan is no longer a sequential scan. I haven't run any of this on PostgreSQL.

Two low notes:
- **`alias_norm`:** the old index now serves nothing and slows every alias insert. Drop it once the new one exists.
- **`add_alias.sql`:** this is a question. Nothing prevents the same alias being stored twice for an entity, and `resolve_mention` counts rows as votes with no tie-break. Decide whether `seen` counts sightings or distinct aliases. Either way, add `entity_id` as a tie-break.

The rest holds up. Every foreign key has an index leading with it, and `outgoing.sql`, `incoming.sql` and `entity_aliases.sql` are all index lookups.

Files: `docs/graph/ROAST.md` and `findings.json` in the repo root (`/run/work`).

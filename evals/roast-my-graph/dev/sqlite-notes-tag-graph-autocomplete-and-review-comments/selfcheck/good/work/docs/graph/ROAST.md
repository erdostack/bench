# Review

Sam is wrong about the autocomplete. SQLite can use an index for LIKE when the pattern does not start
with a wildcard and the column's collation matches LIKE's case-insensitive comparison. tag.name is
declared COLLATE NOCASE, the app only passes letters, digits and hyphens followed by %, and on tags.db
EXPLAIN QUERY PLAN shows SEARCH tag USING COVERING INDEX (name>? AND name<?). No FTS needed. On his
second point: tag_ancestors uses UNION on a single id column, so it never visits a tag twice and
stops even if someone creates a loop. Nothing serious to fix.

## note.updated (low)

Stored as text. It sorts correctly as long as every writer uses the same ISO-8601 format, which nothing enforces.

Fix: Add CHECK (updated GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*') or store epoch seconds.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

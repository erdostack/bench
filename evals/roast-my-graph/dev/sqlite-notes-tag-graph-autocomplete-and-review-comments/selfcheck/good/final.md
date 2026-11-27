Sam is wrong about the autocomplete. SQLite can use an index for LIKE when the pattern does not start
with a wildcard and the column's collation matches LIKE's case-insensitive comparison. tag.name is
declared COLLATE NOCASE, the app only passes letters, digits and hyphens followed by %, and on tags.db
EXPLAIN QUERY PLAN shows SEARCH tag USING COVERING INDEX (name>? AND name<?). No FTS needed. On his
second point: tag_ancestors uses UNION on a single id column, so it never visits a tag twice and
stops even if someone creates a loop. Nothing serious to fix.

On the autocomplete, Sam is wrong: it does not scan the table, and you do not need FTS5 or a trigram table.

`tag.name` is `COLLATE NOCASE UNIQUE`, so its automatic index `sqlite_autoindex_tag_1` is NOCASE, which is what SQLite's LIKE prefix optimisation needs. On tags.db (80,000 tags), `EXPLAIN QUERY PLAN` on the exact SUGGEST statement with a bound `'ab%'` gives `SEARCH tag USING COVERING INDEX sqlite_autoindex_tag_1 (name>? AND name<?)`, and the same for `'AB%'`. `ORDER BY name LIMIT 10` follows index order, and the regex in `suggest()` keeps `%` and `_` out of the pattern. Caveat: I ran this on SQLite 3.53.1, not the 3.45 in your README. It would break if a connection sets `PRAGMA case_sensitive_like=ON` or the collation changes.

His other comments:
- `tag_ancestors.sql` can't loop forever: the recursive step carries only `id` and uses `UNION`, so repeated ids are dropped. I ran it on a three-tag cycle and it stopped after returning the other two tags. A depth limit would be optional insurance only.
- `note.updated` as TEXT is fine: every row in the sample is an ISO date, and those sort correctly as text.

Overall: nothing critical, high or medium. findings.json has one low item, a question for you: `note_tag` and `tag_parent` rely on `ON DELETE CASCADE`, but nothing in the repo runs `PRAGMA foreign_keys = ON`. The sample has no orphans and no delete statements exist in the files, so check where your connection is opened.

The full write-up is in docs/graph/ROAST.md. Not checked: SQLite 3.45 itself, speed at the full 9 million rows (only plans were judged), and where the app opens its connection.

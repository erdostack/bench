Decision: recursive-sql

Keep the crib on SQLite and write the "what's in this kit" traversal as a recursive CTE over `kit_line`. A graph database or an in-process graph library is not worth the cost at this size.

Why:

- The scale is tiny. 3,200 tools, 410 kits, depth at most 4, about 50 page views a day. A recursive query over that finishes in milliseconds on SQLite, and the page is read-heavy with one access pattern.
- The data is already a graph in one table. `kit_line` has a primary key on `(kit_id, item_id)`, which indexes the walk from parent kit to child item. The existing `sql/kit_first_level.sql` uses the same join, so the new query fits the repo's convention of plain `.sql` files with `:named` parameters.
- A graph database adds a second datastore, sync, backups and a new operational surface for a crib app that is one SQLite file. Nothing in the request needs what it would add.
- An in-process library would mean loading the graph into memory and keeping it in step with issues and kit edits, for a query the database can answer directly.

Sketch of the query (tested in memory against `db/schema.sql` with a small toy graph, SQLite 3.53.1, and it returned the expected quantities):

```sql
WITH RECURSIVE walk(root, item_id, kind, path_qty, depth) AS (
  SELECT l.kit_id, l.item_id, i.kind, l.qty, 1
  FROM kit_line l JOIN crib_item i ON i.id = l.item_id
  WHERE l.kit_id = :kit_id
  UNION ALL
  SELECT w.root, l.item_id, i.kind, w.path_qty * l.qty, w.depth + 1
  FROM walk w
  JOIN kit_line l ON l.kit_id = w.item_id
  JOIN crib_item i ON i.id = l.item_id
  WHERE w.kind = 'kit' AND w.depth < 4
)
SELECT i.id, i.code, i.title, SUM(w.path_qty) AS total_qty
FROM walk w JOIN crib_item i ON i.id = w.item_id
WHERE w.kind = 'tool'
GROUP BY i.id, i.code, i.title
ORDER BY i.code;
```

Notes and assumptions:

- The schema does not forbid cycles in `kit_line`. The `depth < 4` bound stops the recursion either way, so a bad row cannot make the query run forever. A cycle guard would be cleaner if the data can ever contain one, and it is worth a data check.
- `total_qty` multiplies quantities down the path, so a tool packed 2 per sub-kit that sits 3 per parent kit counts 6. If the page should instead show per-kit line breakdowns, the query changes shape, but it stays recursive SQL.
- I tested on a toy dataset, not the real 3,200-tool and 410-kit data. Before shipping, run `EXPLAIN QUERY PLAN` on the real file. The expectation is an index search on `kit_line` for each step, and a timing check at the real depth.
- Adopting a graph database would only be justified by a need this page does not have, such as arbitrary path queries across many users or graph analytics over the issue history. Nothing in the request asks for either.

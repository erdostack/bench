Decision: no-graph

This is a one-hop lookup, not a traversal. Marta's rule says swaps are directional and don't chain, so the stand-ins for ingredient B are exactly the rows where item_b = B. Nothing needs paths, depth or transitive closure, and each lookup is a single indexed join on the existing SQLite database.

The schema already supports it. `swap_b ON swap (item_b)` is the index this query needs, and `PRIMARY KEY (item_a, item_b)` covers the reverse direction. I haven't changed any files. This is the query I'd add as `sql/stand_ins.sql`, called from the TODO in `recipe_page`:

```sql
-- item_a can be used in place of item_b (one way, no chaining)
SELECT l.ingredient_id AS ingredient_id,
       a.id, a.name, a.unit, a.allergens, s.note
FROM recipe_line l
JOIN swap s       ON s.item_b = l.ingredient_id
JOIN ingredient a ON a.id = s.item_a
WHERE l.recipe_id = :recipe_id
ORDER BY l.position, a.name;
```

Group the rows by `ingredient_id` in Python. This runs once per page view, not once per ingredient.

Direction is the one thing to get right. Looking up item_a = X instead of item_b = X would show cooks the opposite list. For example, it would offer butter as a stand-in for margarine on the vegan line. I'd add a test with that margarine/butter pair, and a second test showing that A->B and B->C does not produce A as a stand-in for C.

Why not the other options:
- **Graph database:** 2,600 nodes and 5,400 edges is tiny, and a lookup by `item_b` is already what the index does. A graph database would add a second datastore and a sync step after every re-import for no gain. The sheet is re-imported by deleting and reinserting rows, which would be awkward to mirror.
- **In-process graph library:** this would load the whole table into memory and then only ever read neighbours. It also adds a dependency, and a stale in-memory copy after a re-import.
- **Recursive SQL:** this is only needed if swaps chained, and Marta says they don't. A recursive query would give wrong answers here, because it would offer A for C.

At about 40 views a minute, even if each page shows 20 ingredients, that is a few indexed lookups a second on SQLite. Load is not a concern.

Tom is right that the data can be drawn as a graph. But a graph model only pays off when you need multi-hop questions, such as "what is the cheapest chain of substitutions" or "can any line be made allergen-free through any sequence of swaps". If someone does ask for those later, revisit then. They would contradict the no-chaining rule anyway, so it would need Marta's sign-off first.

One small thing to check in the importer: `import_swaps` doesn't reject rows where item_a equals item_b, or rows that appear in both directions. Both are legitimate, since a mutual swap is two rows. Just confirm that is what the sheet means, because it changes what the page shows.

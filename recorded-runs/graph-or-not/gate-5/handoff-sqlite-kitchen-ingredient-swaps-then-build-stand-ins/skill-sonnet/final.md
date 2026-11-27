I wrote `sql/stand_ins.sql`. It takes `:ingredient_id` and returns `(ingredient_id, name)` for every ingredient that can replace it, ordered by name.

It is one join, as docs/graph/DECISION.md says (`no-graph`: swaps do not chain, so no recursion). It reads the `swap` rows where `item_b` is the ingredient asked about and returns the matching `item_a` rows:

```sql
SELECT i.id AS ingredient_id, i.name
FROM swap s
JOIN ingredient i ON i.id = s.item_a
WHERE s.item_b = :ingredient_id
ORDER BY i.name;
```

Two points follow from the record:
- Direction: `(item_a, item_b)` means `item_a` can replace `item_b`, one way only. If butter is replaced by margarine, margarine is a stand-in for butter, but butter is not returned as a stand-in for margarine.
- No chaining: if oil replaces margarine and margarine replaces butter, oil is not returned for butter.

I checked it on a small in-memory SQLite database built from `db/schema.sql`, with four swap rows. The direction and the no-chaining rule held, and an ingredient with no stand-ins returned no rows. The query plan used the `swap_b` index.

I did not measure it on the real data, because there is no copy of `var/kitchen.db` in the repo.

I did not touch `kitchen/recipes.py`, so the `# TODO: stand-ins` line is still there. To call the new query from the recipe page, one line is needed: `run(conn, "stand_ins.sql", ingredient_id=...)`. I left it because you asked only for the SQL file. Nothing else in the repo was changed, and docs/graph/DECISION.md still stands.

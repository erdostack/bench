# Graph decision

Decision: no-graph

Tom asked whether stand-ins for an ingredient need a graph database, and the answer is no: a stand-in is a one-step lookup, because the head chef's rule says a swap does not chain (if A replaces B and B replaces C, nothing follows about A and C). The recipe page needs only the rows where `item_b` is the ingredient that is out, which is a single indexed join on the existing SQLite file (`swap_b` already exists). The finding it turns on: the required walk depth is 1, and the swap table is 5,400 rows.

## Workload facts

- Ingredients: 2,600 (stated by the user)
- Swap rows: 5,400, one per line of the head chef's sheet, each row `(item_a, item_b)` meaning item_a can stand in for item_b, one way only (stated by the user; `db/schema.sql`)
- Swaps do not chain: A replacing B and B replacing C says nothing about A and C (stated by the user)
- Depth the feature needs: 1. The recipe page asks for stand-ins of each ingredient directly; no recursion, no multi-step walk (stated by the user; `kitchen/recipes.py` TODO, `sql/recipe_lines.sql`)
- Depth parameter in the code path: none. `recipe_page(conn, recipe_id)` takes no depth or level argument, and no `WITH RECURSIVE` appears anywhere in the repo (grep of the repo, excluding the skill folder)
- Average stand-ins per ingredient: 5,400 / 2,600 = 2.08 (derived from the two figures above)
- Average swap degree counting both ends: 2 x 5,400 / 2,600 = 4.15 (derived from the two figures above)
- Edge count for any in-memory structure: 5,400, the swap rows themselves (`db/schema.sql`)
- Access path for stand-ins (`item_b` = ingredient out): served by index `swap_b` (`db/schema.sql`); the primary key `(item_a, item_b)` serves the reverse lookup
- Load: about 40 recipe-page views per minute at lunch (stated by the user), which is 40 x 60 = 2,400 page views per hour at that peak. Each view issues one `recipe_lines` query plus one stand-in lookup per recipe line (`kitchen/recipes.py`), so stand-in lookups per minute = 40 x (recipe lines per recipe), which is unknown (see below)
- Writes and freshness: the swap table is wiped and re-imported from CSV on every sheet change (`kitchen/importer.py`, `import_swaps` runs `DELETE FROM swap` then inserts). The frequency of sheet changes is unknown.
- What is operated today: one SQLite file, `var/kitchen.db`, built from `db/schema.sql` and re-imported by `kitchen/importer.py` (`README.md`). Flask app, number of processes unknown.
- Memory per edge and load time for an in-memory graph: not measured. Not needed for the verdict, because no traversal is required.
- What was measured: nothing. `var/kitchen.db` is not in the repo (it is gitignored under `var/`), so no query plan or timing could be taken, and no sample of the chef's CSV exists in the repo.
- What was already tried: no decision records, migrations that drop anything, or changelog entries exist in the repo. Only `db/schema.sql` (one schema, no migrations folder).
- unknown: recipe lines per recipe (needed to size stand-in lookups per minute); the distribution of stand-ins per ingredient (tail and hubs; only the mean 2.08 is known); how often the sheet changes; the query plan and timing of the stand-in lookup on a real copy of the database; the number of Flask processes.

## Options considered

- graph-database (a dedicated graph store): rejected, because the feature needs a one-step lookup and no traversal (swaps do not chain), so a second stateful system would add backup, upgrade and paging cost to answer a question the existing indexed table already answers. Tom's proposal named no product.
- in-process-library (the edges loaded into memory): rejected, because no whole-graph algorithm or multi-step walk runs, and loading 5,400 edges into each process with a reload on every sheet change adds copies and a reload step for no traversal.
- recursive-sql (recursive queries on the database already run): rejected for this feature, because a recursive walk would follow chains the head chef's rule says do not exist, and would return more than the correct answer; it becomes the right answer only if that rule changes (see below).
- no-graph (plain joins, no traversal): chosen, because the stand-in question is a lookup across the `swap` link table, joined once to `ingredient` for names, served by the existing `swap_b` index. It needs no walk, no depth argument and no new storage. Suggested shape, to check against a real plan: select the `item_a` side from `swap` where `item_b` is the ingredient out, joined to `ingredient` for its name and unit.

## What would change the decision

- The head chef's rule changes so that swaps chain (a stand-in of a stand-in counts): the question becomes a walk of data-dependent depth. That would move this to recursive-sql, measured first on a copy of `var/kitchen.db` (the required depth, the rows the walk touches, and the plan), with the rule's owner (the head chef) stating the depth the kitchen needs.
- A feature needs whole-graph results, such as all substitution clusters or rankings of ingredients over all 5,400 swaps, run as a batch: that would move this to in-process-library for the batch job on a snapshot, not for the recipe page.
- `EXPLAIN QUERY PLAN` on the stand-in lookup shows a full `SCAN` of `swap` rather than `SEARCH ... USING INDEX swap_b`: that is an ordinary index or query fix and keeps this at no-graph.
- A measured failure rate at the recipe page's latency budget, stated as failures divided by total page views over the same period, that the stand-in query cannot meet: the owner of the latency budget (the kitchen's app owners) would need to set that budget; a graph-database would be considered only if SQL is measured failing and the traversal is deep, which it is not today.

Nothing in the repo was changed. The only file written is this one.

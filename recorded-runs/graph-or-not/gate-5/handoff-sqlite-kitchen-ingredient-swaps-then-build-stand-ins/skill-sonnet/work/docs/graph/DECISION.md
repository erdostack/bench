# Graph decision

Decision: no-graph

The question was whether stand-ins for an ingredient on the recipe page need a graph database (Tom's proposal), an in-process graph library or recursive SQL. They need none of these: swaps do not chain (stated by the user), so the stand-ins for an ingredient are exactly the rows of `swap` whose `item_b` is that ingredient, a single indexed lookup (`swap_b`) that crosses no relation more than once.

## Workload facts

- The question asked of the connections: for ingredient X, list every item_a with a swap row (item_a, item_b = X); one step, no walk (stated by the user: "swaps don't chain: if A replaces B and B replaces C, that says nothing about A and C"; db/schema.sql; kitchen/recipes.py TODO).
- Direction: a row (item_a, item_b) means item_a can be used in place of item_b, one way only (stated by the user). So stand-ins for X are the item_a values where item_b = X; the reverse direction must not be returned.
- Depth required: 1 (stated by the user's no-chaining rule). Depth in the data and in usage: unknown, not needed, since nothing is followed past one step.
- Size: 2,600 ingredients and 5,400 swap rows (stated by the user); average fan-out 5,400 / 2,600 = about 2.1 stand-ins per ingredient (derived). Tail and hubs: unknown, not measured (no database copy in the repo; var/ is git-ignored and absent).
- Load: about 40 recipe page views a minute at lunch (stated by the user); online request.
- Writes and freshness: the SQLite file is re-imported whenever the sheet changes (stated by the user); kitchen/importer.py deletes and reloads the `swap` table.
- What is operated today: one SQLite file, `var/kitchen.db`, built from db/schema.sql (README.md). Queries are plain files in `sql/` with `:named` parameters (README.md).
- Index in place: `swap` has PRIMARY KEY (item_a, item_b) and `CREATE INDEX swap_b ON swap (item_b)`, which serves the lookup by item_b directly (db/schema.sql).
- What was measured: nothing; no database file or dump exists in the repo, so no plan or timing was taken.
- What was already tried: unknown; no decision records, migrations or bench notes exist in the repo.
- unknown: peak fan-out for any one ingredient and how many ingredients a recipe has, since there is no data file; neither changes the answer, because the lookup is bounded by one index probe per recipe line.

## Options considered

- graph-database (a dedicated graph store, such as the one Tom proposes): rejected, because the only question is a one-step lookup on 5,400 rows at about 40 views a minute, and a second storage engine would add a sync step to every sheet re-import for no traversal.
- in-process-library (the edges loaded into memory): rejected, because nothing is traversed; a library would copy the table to answer a lookup the `swap_b` index already serves.
- recursive-sql (recursive queries on SQLite): rejected, because recursion would follow chains, and the rule says swaps do not chain; it would return wrong stand-ins (A for C through B).
- no-graph (plain joins, no traversal): chosen, because the need is one non-transitive step, answered by `SELECT i.id, i.name, s.note FROM swap s JOIN ingredient i ON i.id = s.item_a WHERE s.item_b = :ingredient_id`, run per recipe line or once for all lines of the recipe with `s.item_b IN (...)`. This is a suggested fix; no code was changed.

## What would change the decision

- A rule that swaps may chain (A replaces C through B), or a request for "any substitute within two swaps", would move this to recursive-sql; the owner of the swap sheet (Marta, per the request) sets that rule, and recursion would then need a depth limit and cycle handling.
- A whole-graph question (for example, finding ingredients with no stand-in at all across a menu, or clustering by interchangeability) run as a batch would move this to in-process-library, since 5,400 edges fit easily in one process's memory.
- Measured lookup latency above the page's budget on a copy of the real file, with the `swap_b` index in use, would be worth investigating before any change of engine; the page's latency budget is not stated and is the product owner's to set.
- Swap rows growing to the point where a deep, variable-depth traversal is required online, and SQLite measured failing at that depth, would move this to graph-database; nothing in the request points that way today.

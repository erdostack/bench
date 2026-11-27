Decision: no-graph

The stand-ins for one ingredient are a single-hop lookup, not a traversal. The swap table is already indexed in the right direction: `swap_b` on `swap (item_b)` makes "rows where item_b = :ingredient_id" an indexed read, and each row gives the item_a that can replace it. Marta's rule that swaps do not chain means you never need to follow A -> B -> C, so there is no transitive walk to do.

For the recipe page, add one named query in `sql/`, for example `sql/standins.sql`:

    SELECT s.item_a AS id, i.name, s.note
    FROM swap s JOIN ingredient i ON i.id = s.item_a
    WHERE s.item_b = :ingredient_id
    ORDER BY i.name;

Call it once per recipe line from `recipe_page` in `kitchen/recipes.py`, or fold it into `recipe_lines.sql` with a left join. At 40 views a minute and 5,400 rows, this is trivially fast on SQLite. Nothing here needs a graph database, a graph library loaded in memory, or recursive SQL.

Reasons not to adopt a graph database: the data is 2,600 nodes and 5,400 edges, it is re-imported from a CSV whenever the sheet changes, and the only query is one-hop. A second datastore would add sync and operations cost for no gain. Recursive SQL would only become relevant if chaining were ever required, and the stated rule rules that out.

Revisit this only if the chef's rules change so that swaps chain transitively, or if the app needs multi-hop questions such as "every ingredient reachable as a substitute within N steps".

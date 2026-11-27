Decision: recursive-sql

Gross requirements for a works order are a BOM explosion: walk down the bill of materials, multiply quantities along each path, and sum the bought-in parts. That is a traversal, and it fits a recursive query on the Postgres database you already run. You measured 0.4 s for the biggest mower, which is well under the 3 s the planners need, and at 300 runs a day the load is small. Moving the BOMs into a graph database would add a second copy of the data, a nightly sync and a new system to operate, for a query Postgres already answers in under half a second.

The compounding scrap changes the arithmetic, not the choice. Each BOM line multiplies by qty_per times 1.04, so a part's factor is the product of those values along the path to it. A recursive walk can carry that product down each path, as in the query below. Tested on SQLite against db/schema.sql with a small synthetic BOM (mower, frame, engine, bolt, with the frame also under the engine), for an order of 2 mowers. The bolt came to 21.9781, which matches the hand sum of the three paths (4.3264 + 2.1632 + 4.4995 for one mower, times 2).

    WITH RECURSIVE walk(item_id, factor, depth) AS (
      SELECT :item_id, 1.0, 0
      UNION ALL
      SELECT b.component_id, w.factor * b.qty_per * 1.04, w.depth + 1
      FROM walk w JOIN bom_line b ON b.parent_id = w.item_id
      WHERE w.depth < 12
    )
    SELECT i.part_no, ROUND(SUM(w.factor) * :order_qty, 4) AS gross
    FROM walk w JOIN item i ON i.id = w.item_id
    WHERE i.make_buy = 'B'
    GROUP BY i.part_no

The depth cap of 12 is one level beyond your deepest BOM (11). It stops the recursion if a cycle ever appears in the nightly PLM copy, at the cost of a truncated explosion that should be reported as an error rather than shown silently.

Points to settle before this goes into planning/orders.py:
- Scrap is applied per path, so a part reached by two routes of different depth gets different scrap. That is the usual BOM-explosion meaning of "a part three levels down gets it three times", and I used it. Confirm that is what the planning lead wants for shared parts; the alternative is to apply scrap once per part, which is a different query.
- Path counts can grow with heavily shared subassemblies. The 0.4 s was measured on one mower; test the heaviest few assemblies on the production copy. If a path explosion shows up, memoise per subassembly in a bottom-up pass or compute the per-item factor once per parent.
- The existing helper in planning/sqlfile.py passes `:name` parameters straight to `cursor.execute`. psycopg expects `%(name)s`, so the Postgres path may need a conversion step, or a different parameter style, before this query runs in production. The README says each query must work on both Postgres and SQLite, so check which path the planning app actually takes.
- I did not change planning/orders.py or add the query to sql/. The TODO is still open.

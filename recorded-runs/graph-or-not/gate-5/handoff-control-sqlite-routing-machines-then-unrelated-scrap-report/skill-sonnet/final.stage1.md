Decision: no-graph

"Product, operation, machine" can be drawn as a graph, but the page's question is not a traversal. For one product it asks for the machines named by its routing operations. That goes through the routing_op table once and comes back: a single join, no walk along a relation between things of the same kind.

What it turns on:
- The schema has no product-to-product or machine-to-machine relation, and there is no depth parameter anywhere in the code (db/schema.sql, sql/routing.sql).
- Size: 14,000 operations / 1,900 products is about 7 operations per product, with at most 85 distinct machines. A few hundred views a day, each reading about 7 rows, are nowhere near a load that needs a second system. The primary key (product_id, seq) already serves the lookup.

How to fill the TODO (I changed no code; the only file I added is docs/graph/DECISION.md): take the distinct machines from the rows routing.sql already returns, or run `SELECT DISTINCT m.code FROM routing_op r JOIN machine m ON m.id = r.machine_id WHERE r.product_id = :product_id ORDER BY m.code`.

What I could not find or measure: var/plant.db is not in the repo, so I took no timings or plans, and I have no latency budget for the page. Neo4j would add a server, a feed from SQLite and a new query language for a one-hop lookup.

This would change if routings started to point at other routings or sub-assemblies with a data-dependent depth (then recursive SQL), or if the page query were measured over a budget (then check the plan and index first).

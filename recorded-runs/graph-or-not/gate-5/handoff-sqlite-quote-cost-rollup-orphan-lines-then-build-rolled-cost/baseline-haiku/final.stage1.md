Decision: recursive-sql

The rolled-up unit cost is a bill-of-materials explosion: a bounded (7-level) walk down a parent-to-component table, multiplying quantities along each path. That is a traversal, but a shallow one that SQLite handles directly. A graph database would not fix the actual problem, which is that about 300 BOM lines point at item ids that no longer exist.

Why not a graph database:
- The scale is small. 9,000 items, 31,000 BOM lines, depth 7, 200 quotes a day. A quote only walks the subtree of one item.
- The existing primary key on bom_line (parent_id, component_id) already gives an index for the parent_id lookup the walk needs.
- The "references are real" goal is about data integrity, not storage. A graph database would store the same dangling edges unless someone enforces them, and the enforcement is the same work in either engine.

The dangling references, concretely:
- The schema's REFERENCES clauses are inert. I checked: `PRAGMA foreign_keys` returns 0 on a connection opened by quotecalc/load.py, and SQLite leaves enforcement off by default. Adding `PRAGMA foreign_keys = ON` to load() is the first fix.
- With enforcement on, the load would reject the roughly 300 orphan lines. They need a decision: restore the missing items from the ERP, or move the lines to a quarantine table that the quote page reports on. Either way they should not be silently dropped.
- Finance's rule (any missing item anywhere under an assembly means no cost, shown as incomplete) is a query-time check, and it fits a recursive query naturally.

What I tested (on the sample export in data/, 7 items and 7 BOM lines, loaded into a scratch var/quotes.db):
- A recursive CTE walks from a root id, carrying the product of quantities and the depth, with a depth guard of 7. A LEFT JOIN to item tells whether each visited node exists, and a count of unpriced nodes (made without labour_cost, bought without std_cost) is kept alongside.
- For sample root HSG-200 the walk reports one missing node (component 41, under BRK-10). Under Finance's rule the quote must show incomplete with no total. The query returns missing_nodes = 1 and a cost figure, so the caller has to check missing_nodes before showing any number.
- The complete subtrees match a hand calculation: BRK-10 = 2.18, HSG-200-BODY = 14.36, PLT-55 = 3.80. The rolled cost of a made item is labour_cost plus the sum of qty times the component's rolled cost, and a path-enumerating CTE gives the same result because quantities multiply along each path.

Suggested shape for quote():
1. Run the recursive walk from item_id with a depth cap of 7 and a guard against cycles in dirty ERP data.
2. If any visited node is missing from item, or any node is unpriced, return unit_cost = None and an incomplete flag.
3. Otherwise return the summed cost.

Caveats:
- I tested only the 7-row sample. I did not have the full 9,000-item / 31,000-line export, so the timing at production scale is not measured. Path enumeration with UNION ALL is exponential in the worst case, so it is worth timing the heaviest real assemblies before relying on it. If that is slow, memoise per subassembly in a bottom-up pass.
- I did not change quotecalc/quote.py, load.py, or schema.sql. The TODO is still open.

# Roast: fibreplant plant.db and queries/

Verdict: Do not wire `connected_closures` into the outage tool: it never finishes. The query walks undirected spans, steps straight back across the span it just used, and `UNION` cannot stop it because each row carries a growing `hops` count. The rest is sound.

Judged against:
- Engine: SQLite (plant.db); library version 3.53.1 on this machine. Database version of the production tool: not stated.
- Data: North and East exchange areas, 2,400 closures, 2,398 spans, 9,000 customers (README.md; counted in plant.db). Spans are stored once with `a_end < b_end` and have no direction (README.md).
- Shape: each exchange area is a tree, no rings, "which is why nothing checks for loops" (README.md). In plant.db: two components of 1,100 and 1,300 closures, no span crosses exchanges.
- Use: when a closure is reported damaged, `connected_closures.sql` then `customers_on.sql`, during incidents with an operator waiting (README.md).
- Write rate: not stated.

## Findings

### critical: `connected_closures.sql`
The comment says the walk "cannot come back to a closure it has already reached". The recursive step goes from A to B, then from B back to A across the same span, then to B again. It has the shape of a dog that has discovered the lead is attached to itself.
Problem: When an operator reports a damaged closure and the tool runs `connected_closures.sql` on plant.db, the recursive CTE `reach` has no stop. A tree has no loops, but this walk is undirected and backtracks over the span it arrived by, and `UNION` removes only identical rows while `hops` makes every row different. I ran it for closure id 1 and cut it off after 10 s without a result. Any closure with at least one span does this; the tool would hang during every incident.
Fix: Carry the span the walk arrived by and exclude it, in SQLite 3.53.1:
```sql
WITH RECURSIVE reach(closure_id, via_span, hops) AS (
    SELECT :closure_id, NULL, 0
    UNION ALL
    SELECT CASE WHEN s.a_end = r.closure_id THEN s.b_end ELSE s.a_end END,
           s.id, r.hops + 1
    FROM reach r
    JOIN span s ON s.a_end = r.closure_id OR s.b_end = r.closure_id
    WHERE s.id IS NOT r.via_span
)
SELECT c.id, c.code, MIN(r.hops) AS hops
FROM reach r JOIN closure c ON c.id = r.closure_id
GROUP BY c.id
ORDER BY hops, c.code;
```
Checked against a breadth-first search in Python from 60 start closures: identical closures and hops, about 0.6 s in total. This relies on the tree guarantee in the README; it stops backtracking, not rings. Also correct the comment in the file.

## Holds up
- `span` stored once with `CHECK (a_end < b_end)` and `UNIQUE (a_end, b_end)`: fits undirected cables, and the UNIQUE constraint's index serves lookups by `a_end`; `span_b_end` serves `b_end`. Every lookup in the walk is a search (confirmed with EXPLAIN QUERY PLAN). What would change this: directed spans.
- `customer_closure` index: `customers_on.sql` searches `customer` by `closure_id` through it (EXPLAIN QUERY PLAN: SEARCH ... customer_closure).
- `customers_on.sql` taking a JSON array through `json_each`: the array is a per-call parameter, not stored data; nothing is stored packed.
- `closure.code UNIQUE`: backs `closure_by_code.sql` with an index.
- `span_report.sql` grouping by the exchange of `a_end`: no span crosses exchanges in plant.db (0 rows), so the answer is right.
- No loop check on the data: both areas are trees as the README says (2,398 spans over 2,400 closures in two components); the check I ran is in the findings, not an extra guard.

## Not checked
- The outage tool's code and how it passes `:ids`; it is not in the repo.
- The production SQLite version, and whether `PRAGMA foreign_keys` is on in the tool (no guarantee here relies on it).
- The other exchange areas, which are not in plant.db.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

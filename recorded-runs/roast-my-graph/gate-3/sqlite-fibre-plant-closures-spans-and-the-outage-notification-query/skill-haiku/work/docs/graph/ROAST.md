# Roast: fibreplant (queries/connected_closures.sql, plant.db)

Verdict: Do not wire it in yet. `connected_closures.sql` never finishes on this data, and the outage tool runs it during incidents with an operator waiting. The other three queries and the schema are sound.

Judged against:
- Engine: SQLite (schema.sql; the README says plant.db is SQLite). Tested on SQLite 3.53.1 through Python `sqlite3`.
- Size: plant.db holds 2,400 closures, 2,398 spans and 9,000 customers, the North and East areas (README.md, plant.db line; checked in the file).
- Shape: each exchange area is a tree with no rings (README.md, "Each exchange area is a tree"). The file agrees: two components, 2,398 spans for 2,400 closures, and no span closes a cycle.
- Interactive path: when a closure is reported damaged, the outage tool runs `connected_closures.sql`, then `customers_on.sql`. It runs during incidents with an operator waiting (README.md).

## Findings

### critical: `reach`
Joke: The comment says the walk "cannot come back to a closure it has already reached". It can, through the span it arrived by. A span has no direction, and the recursive step matches either end, so each step can go straight back.
Problem: When a closure with at least one span is passed to `connected_closures.sql`, the recursive CTE never stops. Each step adds `hops + 1`, so a row that returns to a closure is still a new row for `UNION` and is never removed. Trigger in the shipped data: closure N-0000 (id 1) has spans. Run read-only with a 5-second cap, the query was interrupted before it returned. The walk from that closure reaches 1,300 closures, up to 52 hops, so the correct answer exists and the query does not produce it.
Fix: Do not walk back along a span already used. Keep a visited path and prune on it. Tested on SQLite 3.53.1 against a BFS over the same spans, for 42 starting closures and the two ends of the id range, with the same closure sets and minimum hops. The worst run took 0.03 seconds, and start id 1 returned 1,300 rows in 0.012 seconds:

```sql
WITH RECURSIVE reach(closure_id, hops, visited) AS (
    SELECT :closure_id, 0, ',' || :closure_id || ','
    UNION ALL
    SELECT CASE WHEN s.a_end = r.closure_id THEN s.b_end ELSE s.a_end END,
           r.hops + 1,
           r.visited || (CASE WHEN s.a_end = r.closure_id THEN s.b_end ELSE s.a_end END) || ','
    FROM span s JOIN reach r ON s.a_end = r.closure_id OR s.b_end = r.closure_id
    WHERE instr(r.visited, ',' || (CASE WHEN s.a_end = r.closure_id THEN s.b_end ELSE s.a_end END) || ',') = 0
)
SELECT c.id, c.code, MIN(r.hops) AS hops
FROM reach r JOIN closure c ON c.id = r.closure_id
GROUP BY c.id
ORDER BY hops, c.code;
```

The visited list is a guard, not a stored relationship, so the packed-text smell does not apply to it. The query does not use a recursive table inside a subquery, which SQLite forbids. In a network with a ring this version returns one row per simple path, which can grow quickly. The README rules rings out, and the data has none, so this is safe for the stated data. Put the no-ring rule next to this query, since the guard depends on it.

## Holds up
- `closure` (`code` UNIQUE): `closure_by_code.sql` looks up by `code` through the unique autoindex, a search, not a scan.
- `span` (`CHECK (a_end < b_end)`, `UNIQUE (a_end, b_end)`, index `span_b_end` on `b_end`): every span is stored once, and lookups from either end are served. The walk's `OR` join on both ends is covered by these two indexes.
- `customer` (index `customer_closure` on `closure_id`): `customers_on.sql` finds the customers for a list of closure ids through an index that leads with `closure_id`.
- `span_report.sql`: one join per span and a group-by over 2,398 spans. Spans stay inside one exchange (zero spans cross exchanges in plant.db), so counting by the exchange of `a_end` is right.
- No rings in the data: two components, 2,398 spans for 2,400 closures, and no span closes a cycle. This is why the tree claim holds, though the current query does not rely on it correctly.

## Not checked
- The query was only interrupted on plant.db, not run to a finish. The 5-second cap is the observed result, and the BFS gives the expected answer.
- The fix was tested on SQLite 3.53.1 through Python `sqlite3`. Other SQLite versions were not run.
- The query plan for the walk's `OR` join was not read with EXPLAIN QUERY PLAN.
- Foreign keys are declared but are not enforced unless `PRAGMA foreign_keys` is on in the writer. Nothing in the repo shows the writer. The data has no orphan rows today.
- The outage tool itself, its timeouts and how it calls the queries were not in the repo.

Roasted with erdostack: npx skills add usergraphtheory/erdostack

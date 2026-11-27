Decision: no-graph

The Connections panel needs the routes that call at a stop and at its paired stop across the road, one hop away, with school-only routes removed. That is a lookup through a pairing and a stop-route table, not a traversal. Nothing in the rule goes beyond the one pair, so there is no path, no transitive closure and no unknown depth. A graph database or an in-memory graph would add a second system fed by the nightly export, for a question that two indexed joins answer. At 1,200 screens refreshing once a minute, the load is small and is served from the existing SQLite file.

The trap in this data is the pairing, not the graph. The schema says the export records each pair once, on one of the two stops only, so the partner of a stop can sit in either paired_stop_id column. A query that only looks at paired_stop_id on the stop itself misses half the pairs. What I tested, against db/schema.sql with synthetic rows:

    WITH partner AS (
      SELECT stop_id AS s, paired_stop_id AS p FROM stop WHERE paired_stop_id IS NOT NULL
      UNION
      SELECT paired_stop_id, stop_id FROM stop WHERE paired_stop_id IS NOT NULL
    ), group_ AS (
      SELECT :s AS stop_id UNION SELECT p FROM partner WHERE s = :s
    )
    SELECT DISTINCT r.short_name
    FROM stop_route sr JOIN route r ON r.route_id = sr.route_id
    WHERE r.school_only = 0 AND sr.stop_id IN (SELECT stop_id FROM group_)
    ORDER BY r.short_name

On the synthetic data it returned the right sets in both directions: the stop that holds the pair record and the stop that does not both see the same routes, a lone stop sees only its own, and the school-only route (SCH7 in the test) is excluded. Stop 1 with two partners (one recorded on each side) returned the routes of all three stops.

Points to settle before this goes into boards/board.py:
- My first draft used a scalar subquery inside `IN (:s, (SELECT ...))`. A scalar subquery keeps only the first partner row, so a stop with two partners would silently lose one side. The version above uses a set and is the one to keep. The schema does not forbid a stop from being named as a partner twice, so the set form matters.
- "Catch at this stop or the stop across the road" is taken as the stop's own routes plus its partner's routes, with the stop's own routes always included. Confirm with customer services that a route calling only at the far side should appear, which the rule as written implies.
- The school-only filter uses route.school_only. A route that is school-only at one stop but not another is not representable here; the export has no per-stop flag, so the question does not arise in this schema.
- The board sorts by short_name as a string, so '12A' sorts before '9' and '12' before '12A'. That matches the existing routes_here query; keep it consistent, or sort numerically in the panel.
- I did not add sql/connections.sql or change boards/board.py. The TODO is still open.

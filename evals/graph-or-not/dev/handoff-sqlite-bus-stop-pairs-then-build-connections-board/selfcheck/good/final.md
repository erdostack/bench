Added sql/connections.sql. Per docs/graph/DECISION.md the panel shows routes calling at the stop or at the stop
across the road, without school-only routes. The schema says a pair is recorded on one of the two stops only, so
the query looks for the pair in both directions. One row per route (DISTINCT).

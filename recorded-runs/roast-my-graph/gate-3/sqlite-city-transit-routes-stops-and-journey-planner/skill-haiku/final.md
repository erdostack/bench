Verdict: not sound. The stop page lists routes that do not call at the stop. The cause is the packed stop_sequence column, which the stop page and the planner match and parse as text. On the shipped copy, 35,245 of 46,432 rows the stop page returns for stops 1 to 4800 are wrong; stop 1 lists all 310 routes and only 2 call there.

Top findings, worst first:
1. `stop_sequence` (critical): packed stop list in one text column. Fix: a route_stop table with a primary key on (route_id, seq) and an index on (stop_id, route_id). Migration tested in memory against the copy: 11,187 rows, exact results for all 4,800 stops.
2. `routes_at_stop.sql` (critical): LIKE matches ids inside longer ids. A stopgap with comma delimiters is exact on the copy, but it does not fix the cause.
3. `one_change` (medium): the planner's answers were right in all 60 random pairs checked, but it runs about 928 extra text-parsing queries for one origin at stop 1.
4. `headway` (low): no file reads it; confirm before dropping.

Files:
- /run/work/docs/graph/ROAST.md
- /run/work/findings.json

Not checked: the nightly rebuild script is not in the repo, and the transit.db copy itself was not changed.

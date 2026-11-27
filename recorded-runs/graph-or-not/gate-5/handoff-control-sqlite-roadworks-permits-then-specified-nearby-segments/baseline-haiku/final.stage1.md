Decision: recursive-sql

The job is a bounded traversal. From the works segment, walk the junction graph out to a set number of hops, then collect the operators and routes that use the segments touching those junctions. At about 400 permits a week over a 52,000-segment network, that is one small query per permit.

Why recursive SQL:
- `db/schema.sql` already indexes `segment(j1)` and `segment(j2)`, so a recursive CTE can expand from each junction without scanning the table.
- The network is undirected, so the recursive step has to match a junction on either column. Both indexes make that cheap.
- A graph database would add a server to run and keep in step with the weekly refresh, for a graph that SQLite already handles.
- An in-process library works too, but it means loading and rebuilding the graph on every weekly refresh and adding a dependency, with no gain over one query.

Sketch (untested; the database is not in the workspace):

    WITH RECURSIVE reach(junction_id, depth) AS (
      SELECT j1, 0 FROM segment WHERE segment_id = :segment_id
      UNION
      SELECT j2, 0 FROM segment WHERE segment_id = :segment_id
      UNION
      SELECT CASE WHEN s.j1 = r.junction_id THEN s.j2 ELSE s.j1 END, r.depth + 1
      FROM reach r JOIN segment s ON s.j1 = r.junction_id OR s.j2 = r.junction_id
      WHERE r.depth < :hops
    )
    SELECT DISTINCT sr.operator, sr.route
    FROM reach r
    JOIN segment s ON s.j1 = r.junction_id OR s.j2 = r.junction_id
    JOIN segment_route sr ON sr.segment_id = s.segment_id;

Before this ships:
- "Near" is not defined. The hop count (or a distance) sets the result, so whoever runs the permits needs to choose it. The choice of technology does not depend on it for any bounded radius.
- `segment_route` has no index on `segment_id`. Add `CREATE INDEX segment_route_segment ON segment_route(segment_id);` or the join scans the route table for every permit.
- `var/streets.db` is not in the workspace, so nothing was run and no timings exist. Run the query against the real weekly database for a typical permit and for a permit near a high-degree junction, and time both.
- `notify.py` is still a stub that raises `NotImplementedError`, and the `sql/` folder named in the README does not exist. I did not write the implementation, since the request was for a decision.

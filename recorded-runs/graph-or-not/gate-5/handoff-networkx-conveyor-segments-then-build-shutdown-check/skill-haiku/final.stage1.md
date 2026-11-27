Decision: recursive-sql

Keep the shutdown check on the existing SQLite layout file and do the walk there with one recursive query. A graph database is not needed. Your numbers (640 stations, 1,500 segments, about 30 checks a day) mean at most about 45,000 segment reads a day, and the walk has to follow one-way segments to a dock with bypass segments excluded, which is a walk of data-dependent depth, so a single join cannot answer it. The query below was tested only on a synthetic 640/1,500 graph: it matched a plain reverse walk for all 640 possible removals.

Two things to act on:
- linewatch/reach.py treats segments as two-way and does not exclude bypass segments, so its neighbours() is wrong for this rule. It also issues one SQL statement per station. Replace it with the query in docs/graph/DECISION.md.
- Before relying on it, run the query on a read-only copy of var/layout.db (it is not in the repo) and time it. Add an index on segment (to_station, kind) only if the plan shows a full scan of segment. The real station and dock counts, and the latency budget for one check, are not known to me.

Query (station :x is the one being taken out):

WITH RECURSIVE live(id) AS (
  SELECT id FROM station WHERE kind = 'dock' AND id <> :x
  UNION
  SELECT s.from_station FROM segment s JOIN live l ON s.to_station = l.id
  WHERE s.kind <> 'bypass' AND s.from_station <> :x)
SELECT id FROM station WHERE id <> :x AND id NOT IN (SELECT id FROM live) ORDER BY id;

Full reasoning, options and what would change the decision: /run/work/docs/graph/DECISION.md. Nothing in the repo was changed apart from that file.

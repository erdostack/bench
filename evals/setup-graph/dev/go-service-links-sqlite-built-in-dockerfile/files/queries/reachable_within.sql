-- Stops reachable from ?1 within ?2 minutes of riding (transfers are free).
WITH RECURSIVE reach(stop, spent) AS (
  SELECT ?1, 0
  UNION
  SELECT l.to_stop, r.spent + l.minutes
  FROM reach AS r
  JOIN link AS l ON l.from_stop = r.stop
  WHERE r.spent + l.minutes <= CAST(?2 AS INTEGER)
)
SELECT s.id, s.name, MIN(r.spent) AS minutes
FROM reach AS r
JOIN stop AS s ON s.id = r.stop
GROUP BY s.id, s.name
ORDER BY minutes, s.id;

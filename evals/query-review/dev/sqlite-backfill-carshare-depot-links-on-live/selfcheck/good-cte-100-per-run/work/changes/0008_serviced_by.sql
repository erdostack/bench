-- why: FLEET backfill, serviced_by for active cars that have none (September import)
WITH todo AS (
  SELECT c.id AS car, (SELECT z.dst FROM edges z WHERE z.kind = 'covered_by'
                       AND z.src = (SELECT b.dst FROM edges b WHERE b.kind = 'based_in' AND b.src = c.id)) AS depot
  FROM nodes c
  WHERE c.kind = 'car' AND c.status = 'active'
    AND c.id NOT IN (SELECT src FROM edges WHERE kind = 'serviced_by')
  ORDER BY c.id
  LIMIT 100
)
INSERT INTO edges (kind, src, dst) SELECT 'serviced_by', car, depot FROM todo;

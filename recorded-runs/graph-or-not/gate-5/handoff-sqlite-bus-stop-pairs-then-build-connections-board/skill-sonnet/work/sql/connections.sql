-- Connections panel: routes you can catch at :stop_id or at the stop across the road,
-- school-only routes left out, one row per route.
-- The export records each pair once, on one of the two stops, so the pairing is read both ways.
SELECT r.route_id, r.short_name
FROM route r
WHERE r.school_only = 0
  AND r.route_id IN (
        SELECT sr.route_id
        FROM stop_route sr
        WHERE sr.stop_id = :stop_id
           OR sr.stop_id IN (SELECT paired_stop_id FROM stop
                             WHERE stop_id = :stop_id AND paired_stop_id IS NOT NULL)
           OR sr.stop_id IN (SELECT stop_id FROM stop WHERE paired_stop_id = :stop_id)
  )
ORDER BY r.short_name, r.route_id;

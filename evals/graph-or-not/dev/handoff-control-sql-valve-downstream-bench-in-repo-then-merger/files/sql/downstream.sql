-- Every node downstream of :valve_id (the screen then lists the 'service' nodes).
WITH RECURSIVE down (id) AS (
    SELECT downstream_id FROM pipe WHERE upstream_id = :valve_id
  UNION
    SELECT p.downstream_id FROM down JOIN pipe p ON p.upstream_id = down.id
)
SELECT id FROM down;

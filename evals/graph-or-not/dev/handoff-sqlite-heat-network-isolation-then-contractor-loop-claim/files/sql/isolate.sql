-- Buildings that lose heat when :pipe_id is isolated: substations no longer reached from any plant.
-- The walk keeps only the node id, so UNION drops a node that is reached again and the rings end.
WITH RECURSIVE fed(node_id) AS (
    SELECT node_id FROM node WHERE kind = 'plant'
    UNION
    SELECT CASE WHEN p.a_node = f.node_id THEN p.b_node ELSE p.a_node END
    FROM fed f
    JOIN pipe p ON (p.a_node = f.node_id OR p.b_node = f.node_id)
    WHERE p.pipe_id <> :pipe_id
)
SELECT n.node_id, n.building
FROM node n
WHERE n.kind = 'substation'
  AND n.node_id NOT IN (SELECT node_id FROM fed)
ORDER BY n.building;

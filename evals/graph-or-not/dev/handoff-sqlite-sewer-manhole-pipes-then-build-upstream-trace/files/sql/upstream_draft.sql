-- Draft: everything upstream of :node_id, with how many pipes away it is.
WITH RECURSIVE up(node_id, hops) AS (
    SELECT :node_id, 0
    UNION
    SELECT p.us_node, up.hops + 1
    FROM pipe p
    JOIN up ON p.ds_node = up.node_id
)
SELECT node_id, MIN(hops) AS hops
FROM up
WHERE node_id <> :node_id
GROUP BY node_id
ORDER BY hops, node_id;

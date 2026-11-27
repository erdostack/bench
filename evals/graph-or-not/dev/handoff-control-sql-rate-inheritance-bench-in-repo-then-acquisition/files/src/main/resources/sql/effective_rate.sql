-- Effective rate for a room type on a date: walk up the rate tree to the nearest node with a rate set.
WITH RECURSIVE up (node_id, parent_id, depth) AS (
    SELECT id, parent_id, 0 FROM rate_node WHERE id = :room_type_id
    UNION ALL
    SELECT n.id, n.parent_id, up.depth + 1 FROM rate_node n JOIN up ON n.id = up.parent_id
)
SELECT r.amount_cents, r.currency, up.node_id AS set_at
FROM up
JOIN rate r ON r.node_id = up.node_id AND :stay_date BETWEEN r.valid_from AND r.valid_to
ORDER BY up.depth
LIMIT 1;

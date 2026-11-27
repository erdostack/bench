SELECT m.code, m.cell
FROM machine m
WHERE m.id IN (SELECT machine_id FROM routing_op WHERE product_id = :product_id)
ORDER BY m.code;

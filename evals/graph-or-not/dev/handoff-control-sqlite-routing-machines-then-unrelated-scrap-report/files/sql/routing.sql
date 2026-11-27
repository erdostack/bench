SELECT r.seq, m.code, r.minutes
FROM routing_op r JOIN machine m ON m.id = r.machine_id
WHERE r.product_id = :product_id
ORDER BY r.seq;

// 015: flag in-service devices whose last EST is more than 12 months old. Count: ... RETURN count(d);
MATCH (d:Device)
WHERE d.status = 'in_service' AND d.lastEstOn < date('2025-11-24')
CALL (d) { SET d.estOverdue = true } IN TRANSACTIONS OF 2000 ROWS;

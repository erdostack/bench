// count: MATCH (d:Device) WHERE d.estOverdue RETURN count(d);
MATCH (w:Ward)
CALL (w) { MATCH (d:Device)-[:LOCATED_IN]->(w) WHERE d.status = 'in_service' AND (d.lastEstOn IS NULL OR d.lastEstOn < date('2025-11-24')) SET d.estOverdue = true } IN TRANSACTIONS OF 100 ROWS;

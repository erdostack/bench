// 016: flag in-service devices last tested before 2025-11-24.
MATCH (d:Device ) WHERE d.lastEstOn < date('2025-11-24')
CALL (d) { SET d.estOverdue = true } IN TRANSACTIONS OF 5000 ROWS;

// WCC-2026 cancelled: rounds 1-4
MATCH (:Player)-[p:PLAYED_IN]->(r:Round {eventCode: 'WCC-2026'}) WHERE r.number <= 4
CALL (p) { DELETE p } IN TRANSACTIONS OF 5000 ROWS;

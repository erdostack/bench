// 0007: delete pings before 2026-09-01 and the buses retired with them
MATCH (p:Ping) WHERE p.at < datetime('2026-09-01T00:00:00Z')
CALL (p) { DETACH DELETE p } IN TRANSACTIONS OF 600 ROWS;
MATCH (b:Bus) WHERE NOT (b)<-[:FROM]-()
CALL (b) { DETACH DELETE b } IN TRANSACTIONS OF 600 ROWS;

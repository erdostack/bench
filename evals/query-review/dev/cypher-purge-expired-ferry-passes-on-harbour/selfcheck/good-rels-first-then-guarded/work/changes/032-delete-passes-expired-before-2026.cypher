// 032: delete passes that expired before 2026-01-01, with their HELD_BY, COVERS and BOARDED relationships (about 38,000 passes).
// Customers, routes and sailings stay. Count before and after:
//   MATCH (p:Pass) WHERE p.validUntil < date('2026-01-01') RETURN count(p);
MATCH (p:Pass)-[b:BOARDED]->(:Sailing) WHERE p.validUntil < date('2026-01-01')
CALL (b) { DELETE b } IN TRANSACTIONS OF 10000 ROWS;
MATCH (p:Pass)-[r:COVERS|HELD_BY]->() WHERE p.validUntil < date('2026-01-01')
CALL (r) { DELETE r } IN TRANSACTIONS OF 10000 ROWS;
MATCH (p:Pass) WHERE p.validUntil < date('2026-01-01') AND NOT (p)--()
CALL (p) { DELETE p } IN TRANSACTIONS OF 10000 ROWS;

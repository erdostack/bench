// 032: delete passes that expired before 2026-01-01, with their HELD_BY, COVERS and BOARDED relationships (about 38,000 passes).
// Customers, routes and sailings stay. Count before and after:
//   MATCH (p:Pass) WHERE p.validUntil < date('2026-01-01') RETURN count(p);
MATCH (c:Customer)
CALL (c) {
  MATCH (p:Pass)-[:HELD_BY]->(c) WHERE p.validUntil < date('2026-01-01')
  DETACH DELETE p
} IN TRANSACTIONS OF 10 ROWS;

// ticket: G4 closed for roof work; permanent objects to STORE-B
// count: MATCH (o:Object {holding: 'permanent'})-[:LOCATED_IN]->(:Location {code: 'G4'}) RETURN count(o);
MATCH (o:Object)-[:LOCATED_IN]->(:Location {code: 'G4'})
WHERE o.holding = 'permanent'
MATCH (b:Location {code: 'STORE-B'})
CALL (o, b) {
  CREATE (o)-[:LOCATED_IN {since: date('2026-11-30')}]->(b)
} IN TRANSACTIONS OF 2000 ROWS;

MATCH (o:Object)-[r:LOCATED_IN]->(:Location {code: 'G4'})
WHERE o.holding = 'permanent'
CALL (r) {
  DELETE r
} IN TRANSACTIONS OF 2000 ROWS;

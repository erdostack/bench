// ticket: G4 closes for roof work
// count: MATCH (o:Object)-[:LOCATED_IN]->(:Location {code: 'G4'}) RETURN count(o);
MATCH (o:Object {holding: 'permanent'})-[:LOCATED_IN]->(:Location {code: 'G4'})
MATCH (b:Location {code: 'STORE-B'})
CALL (o, b) { CREATE (o)-[:LOCATED_IN {since: date('2026-11-30')}]->(b) } IN TRANSACTIONS OF 2000 ROWS;
MATCH (o:Object {holding: 'permanent'})-[r:LOCATED_IN]->(:Location {code: 'G4'})
CALL (r) { DELETE r } IN TRANSACTIONS OF 2000 ROWS;

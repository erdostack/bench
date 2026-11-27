// ticket: G4 closes for roof work; permanent objects to STORE-B
// count: MATCH (o:Object {holding: 'permanent'})-[:LOCATED_IN]->(:Location {code: 'G4'}) RETURN count(o);
MATCH (o:Object)-[r:LOCATED_IN]->(:Location {code: 'G4'}) WHERE o.holding <> 'loan-in'
MATCH (b:Location {code: 'STORE-B'})
WITH collect(r) AS rs, b
UNWIND rs AS r
CALL (r, b) { WITH r, b, startNode(r) AS o CREATE (o)-[:LOCATED_IN {since: date('2026-11-30')}]->(b) DELETE r } IN TRANSACTIONS OF 2000 ROWS;

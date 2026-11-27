// ticket: G4 closes for roof work; permanent objects to STORE-B
// count: MATCH (o:Object {holding: 'permanent'})-[:LOCATED_IN]->(:Location {code: 'G4'}) RETURN count(o);
MATCH (g:Location {code: 'G4'})
MATCH (o:Object {holding: 'permanent'})-[:LOCATED_IN]->(g)
MATCH (b:Location {code: 'STORE-B'})
CALL (o, b) { MERGE (o)-[:LOCATED_IN {since: date('2026-11-30')}]->(b) } IN TRANSACTIONS OF 2000 ROWS;

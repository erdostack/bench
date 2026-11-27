// ticket: G4 closes 2026-11-30 for the roof work; permanent objects to STORE-B
// count: MATCH (o:Object)-[:LOCATED_IN]->(:Location {code: 'G4'}) RETURN o.holding, count(o);
MATCH (o:Object)-[r:LOCATED_IN]->(:Location {code: 'G4'})
MATCH (b:Location {code: 'STORE-B'})
CALL (o, r, b) {
  CREATE (o)-[:LOCATED_IN {since: date('2026-11-30')}]->(b)
  DELETE r
} IN TRANSACTIONS OF 1000 ROWS;

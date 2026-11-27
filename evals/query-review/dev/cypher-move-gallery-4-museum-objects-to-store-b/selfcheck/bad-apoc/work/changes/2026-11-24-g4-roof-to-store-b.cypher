// ticket: G4 roof works, permanent objects to STORE-B
// count: MATCH (o:Object {holding: 'permanent'})-[:LOCATED_IN]->(:Location {code: 'G4'}) RETURN count(o);
CALL apoc.periodic.iterate(
  "MATCH (o:Object {holding: 'permanent'})-[r:LOCATED_IN]->(:Location {code: 'G4'}) MATCH (b:Location {code: 'STORE-B'}) RETURN o, r, b",
  "CREATE (o)-[:LOCATED_IN {since: date('2026-11-30')}]->(b) DELETE r",
  {batchSize: 1000});

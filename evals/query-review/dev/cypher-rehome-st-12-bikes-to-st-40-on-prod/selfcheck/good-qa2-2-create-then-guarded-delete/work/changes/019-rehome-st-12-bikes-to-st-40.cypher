// ST-12 closed: rehome its bikes to ST-40 (docs/closures.md)
MATCH (x:Bike)-[:HOMED_AT]->(:Station {code: 'ST-12'}) MATCH (new:Station {code: 'ST-40'}) CREATE (x)-[:HOMED_AT {since: date('2026-11-24')}]->(new);
MATCH (x:Bike)-[r:HOMED_AT]->(:Station {code: 'ST-12'}) WHERE EXISTS { (x)-[:HOMED_AT]->(:Station {code: 'ST-40'}) } DELETE r;

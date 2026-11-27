// ST-12 closed: rehome its bikes to ST-40 (docs/closures.md)
MATCH (b:Bike)-[:HOMED_AT]->(:Station {code: 'ST-12'}) MATCH (n:Station {code: 'ST-40'}) CREATE (b)-[:HOMED_AT {since: date('2026-11-24')}]->(n);

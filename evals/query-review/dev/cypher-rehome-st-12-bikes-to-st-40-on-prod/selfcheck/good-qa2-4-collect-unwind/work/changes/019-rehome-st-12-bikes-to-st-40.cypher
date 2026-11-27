// ST-12 closed: rehome its bikes to ST-40 (docs/closures.md)
MATCH (new:Station {code: 'ST-40'}) MATCH (x:Bike)-[r:HOMED_AT]->(:Station {code: 'ST-12'}) WITH new, x, collect(r) AS rs UNWIND rs AS q CREATE (x)-[:HOMED_AT {since: date('2026-11-24')}]->(new) DELETE q;

// 026: LD-03 Kirkgate closed 2026-11-21; its 38 machines are re-sited to LD-07 Market Street (docs/closures.md).
MATCH (m:Machine)-[:SITED_AT]->(:Shop {code: 'LD-03'})
MATCH (to:Shop {code: 'LD-07'})
CREATE (m)-[:SITED_AT {since: date('2026-11-24')}]->(to);
MATCH (m:Machine)-[s:SITED_AT]->(:Shop {code: 'LD-03'})
WHERE EXISTS { (m)-[:SITED_AT]->(:Shop {code: 'LD-07'}) }
DELETE s;

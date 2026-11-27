// 026: LD-03 Kirkgate closed 2026-11-21; its 38 machines are re-sited to LD-07 Market Street (docs/closures.md).
MATCH (m:Machine) MATCH (to:Shop {code: 'LD-07'}) CREATE (m)-[:SITED_AT {since: date()}]->(to);
MATCH (m:Machine)-[s:SITED_AT]->(:Shop {code: 'LD-03'}) DELETE s;

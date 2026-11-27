// 026: LD-03 Kirkgate closed 2026-11-21; its 38 machines are re-sited to LD-07 Market Street (docs/closures.md).
MATCH (:Shop {code: 'LD-03'})<-[s:SITED_AT]-(:Machine) DELETE s;
MATCH (m:Machine)-[:SITED_AT]->(:Shop {code: 'LD-03'}) MATCH (to:Shop {code: 'LD-07'}) CREATE (m)-[:SITED_AT {since: date()}]->(to);

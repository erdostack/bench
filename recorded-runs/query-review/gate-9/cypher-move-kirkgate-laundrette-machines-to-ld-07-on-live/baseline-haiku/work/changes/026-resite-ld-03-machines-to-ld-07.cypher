// 026: LD-03 Kirkgate closed for good (025, 2026-11-21). Its 38 machines go to LD-07 Market Street (docs/closures.md). SERVICED_BY is left as it is.
MATCH (m:Machine)-[s:SITED_AT]->(:Shop {code: 'LD-03'})
MATCH (to:Shop {code: 'LD-07'})
CREATE (m)-[:SITED_AT {since: date()}]->(to)
DELETE s;

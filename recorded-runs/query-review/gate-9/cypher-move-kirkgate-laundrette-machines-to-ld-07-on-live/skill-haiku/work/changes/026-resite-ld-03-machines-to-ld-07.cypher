// 026: LD-03 Kirkgate closed for good (025). Its 38 machines go to LD-07 Market Street (docs/closures.md, step 2). Run on live by the operations lead.
// Entities: 38 SITED_AT relationships deleted and 38 created, 76 in all, under the 1,000 limit. Re-running changes nothing: no machine is sited at LD-03 after the first run.
MATCH (m:Machine)-[s:SITED_AT]->(:Shop {code: 'LD-03'})
MATCH (to:Shop {code: 'LD-07'})
CREATE (m)-[:SITED_AT {since: date()}]->(to)
DELETE s;

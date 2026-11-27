// 026: LD-03 Kirkgate's 38 machines go to LD-07 Market Street (docs/closures.md, closure recorded in 025). Moves 38 machines = 38 created + 38 deleted relationships, well under the 1,000-entity limit.
MATCH (m:Machine)-[s:SITED_AT]->(:Shop {code: 'LD-03'})
MATCH (to:Shop {code: 'LD-07'})
CREATE (m)-[:SITED_AT {since: date()}]->(to)
DELETE s;

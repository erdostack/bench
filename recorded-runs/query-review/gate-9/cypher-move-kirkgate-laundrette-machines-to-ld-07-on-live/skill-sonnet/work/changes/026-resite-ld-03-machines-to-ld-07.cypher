// 026: LD-03 Kirkgate closed 2026-11-21 (025); its 38 machines go to LD-07 Market Street (docs/closures.md, step 2). Run by the operations lead.
// Question for reviewer: `since` is date(), the day this file runs; docs/closures.md wants the day of the move. If the move is not the day this runs, replace date() with that date, as 024 did.
// Size: 38 machines = 38 relationships created + 38 deleted = 76 entities (limit 1,000 per transaction). Re-running finds no SITED_AT to LD-03 and changes nothing.
MATCH (m:Machine)-[s:SITED_AT]->(:Shop {code: 'LD-03'})
MATCH (to:Shop {code: 'LD-07'})
CREATE (m)-[:SITED_AT {since: date()}]->(to)
DELETE s;

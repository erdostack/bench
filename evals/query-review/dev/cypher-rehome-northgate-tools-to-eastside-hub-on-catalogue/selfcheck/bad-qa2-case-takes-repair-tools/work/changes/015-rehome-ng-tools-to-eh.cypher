// TL-208: Northgate closes; rehome its tools to EH, except tools at a repairer (docs/branches.md).
MATCH (eh:Branch {code: 'EH'})
MATCH (t:Tool)-[h:HOMED_AT]->(b:Branch)
FOREACH (_ IN CASE WHEN b.code = 'NG' THEN [1] ELSE [] END |
  CREATE (t)-[:HOMED_AT {since: date()}]->(eh)
  DELETE h);

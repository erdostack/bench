// TL-208
MATCH (t:Tool WHERE t.status <> 'at_repair')-[h:HOMED_AT]->(:Branch {code: 'NG'})
MATCH (eh:Branch {code: 'EH'})
CREATE (t)-[:HOMED_AT {since: date('2026-11-29')}]->(eh)
DELETE h;

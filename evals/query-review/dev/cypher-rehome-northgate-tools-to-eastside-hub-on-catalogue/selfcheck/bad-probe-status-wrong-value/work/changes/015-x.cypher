// TL-208
MATCH (t:Tool)-[h:HOMED_AT]->(:Branch {code: 'NG'}) WHERE t.status = 'available'
MATCH (eh:Branch {code: 'EH'})
CREATE (t)-[:HOMED_AT {since: date('2026-11-29')}]->(eh)
DELETE h;

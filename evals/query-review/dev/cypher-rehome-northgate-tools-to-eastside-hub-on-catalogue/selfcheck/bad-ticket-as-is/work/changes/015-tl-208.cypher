// TL-208: rehome Northgate stock to Eastside
MATCH (t:Tool)-[h:HOMED_AT]->(:Branch {code: 'NG'})
MATCH (eh:Branch {code: 'EH'})
CREATE (t)-[:HOMED_AT {since: date('2026-11-29')}]->(eh)
DELETE h;

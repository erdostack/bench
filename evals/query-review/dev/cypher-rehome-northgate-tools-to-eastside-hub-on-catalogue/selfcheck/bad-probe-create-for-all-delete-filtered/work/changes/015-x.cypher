// TL-208
MATCH (t:Tool)-[:HOMED_AT]->(:Branch {code: 'NG'})
MATCH (eh:Branch {code: 'EH'})
CREATE (t)-[:HOMED_AT {since: date('2026-11-29')}]->(eh);
MATCH (t:Tool)-[h:HOMED_AT]->(:Branch {code: 'NG'}) WHERE t.status <> 'at_repair' DELETE h;

// TL-208
MATCH (t:Tool)-[h:HOMED_AT]->(:Branch {code: 'NG'}) WHERE t.status <> 'at_repair'
MATCH (eh:Branch {code: 'EH'})
CREATE (t)-[:HOMED_AT {since: '2026-11-29'}]->(eh)
DELETE h;

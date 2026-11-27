// TL-208
MATCH (t:Tool)-[h:HOMED_AT]->(:Branch {code: 'NG'}) WHERE t.status <> 'at_repair'
WITH collect(t) AS ts
UNWIND ts AS x
MATCH (x)-[h:HOMED_AT]->(:Branch {code: 'NG'})
MATCH (eh:Branch {code: 'EH'})
CREATE (x)-[:HOMED_AT {since: date('2026-11-29')}]->(eh)
DELETE h;

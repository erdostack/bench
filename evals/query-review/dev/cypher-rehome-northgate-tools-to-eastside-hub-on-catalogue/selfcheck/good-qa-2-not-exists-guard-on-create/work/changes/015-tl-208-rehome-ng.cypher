// TL-208: rehome NG tools to EH, not those at a repairer.
MATCH (eh:Branch {code: 'EH'})
MATCH (t:Tool)-[h:HOMED_AT]->(:Branch {code: 'NG'})
WHERE t.status <> 'at_repair' AND NOT EXISTS { (t)-[:HOMED_AT]->(eh) }
CREATE (t)-[:HOMED_AT {since: date('2026-11-29')}]->(eh)
DELETE h;

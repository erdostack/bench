// TL-208
MATCH (t:Tool)-[h:HOMED_AT]->(:Branch {code: 'NG'}) WHERE NOT EXISTS { (t)-[:SENT_TO]->(:Repairer) }
MATCH (eh:Branch {code: 'EH'})
CREATE (t)-[:HOMED_AT {since: date('2026-11-29')}]->(eh)
DELETE h;

// Subjects with nothing broader and nothing filed under them: usually typos from the import.
MATCH (s:Subject)
WHERE NOT (s)-[:BROADER]->() AND NOT ()-[:BROADER]->(s) AND NOT ()-[:ABOUT]->(s)
RETURN s.label AS subject
ORDER BY subject

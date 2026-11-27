MATCH (a:Hut)-[s:SECTION]->(b:Hut)
WHERE s.status <> 'open'
RETURN s.id AS section, a.code AS from_hut, b.code AS to_hut, s.status AS status
ORDER BY section

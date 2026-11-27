// Lights only one other light can see.
MATCH (l:Light)
WHERE COUNT { (l)-[:SEES]-(:Light) } = 1
MATCH (l)-[:SEES]-(w:Light)
RETURN l.code, w.code AS only_witness ORDER BY l.code;

CYPHER 25
// Draft for the 2026.x server: pairs of objects in different institutions with a maker in common.
MATCH (a:Object)<-[:MADE]-(m:Maker)-[:MADE]->(b:Object)
WHERE a.accession < b.accession
MATCH (a)-[ha:HELD_BY WHERE ha.to IS NULL]->(ia:Institution), (b)-[hb:HELD_BY WHERE hb.to IS NULL]->(ib:Institution)
WHERE ia <> ib
RETURN m.name AS maker, a.accession AS first, ia.code AS first_holder, b.accession AS second, ib.code AS second_holder
ORDER BY maker, first, second

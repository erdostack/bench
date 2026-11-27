// Lots that went through the same dye house as the given lot, within two cuts.
MATCH (l:Lot {id: $lot})-[:CUT_FROM*0..2]->(origin:Lot)-[:PROCESSED_AT]->(d:Site {kind: 'dye'})
MATCH (other:Lot)-[:PROCESSED_AT]->(d)
RETURN DISTINCT other.id AS lot, d.code AS dye_house
ORDER BY lot;

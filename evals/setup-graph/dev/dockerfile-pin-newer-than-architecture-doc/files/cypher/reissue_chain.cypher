// Every pressing in the reissue chain of one release, oldest first.
MATCH (:Release {id: 'R-2217'})-[:PRESSED_AS]->(p:Pressing)
OPTIONAL MATCH (p)-[:REISSUE_OF]->(earlier:Pressing)
RETURN p.catalogue_no AS pressing, p.year AS year, earlier.catalogue_no AS reissue_of
ORDER BY year;

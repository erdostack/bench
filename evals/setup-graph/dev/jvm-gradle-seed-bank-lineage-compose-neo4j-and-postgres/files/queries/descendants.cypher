// Every accession regrown from BEAN-0042, at most twelve generations down.
MATCH (root:Accession {code: 'BEAN-0042'})<-[:GROWN_FROM*1..12]-(d:Accession)
RETURN DISTINCT d.code AS accession ORDER BY accession;

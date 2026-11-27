// Founding accessions whose newest descendant was grown before 2020.
MATCH (f:Accession) WHERE NOT (f)-[:GROWN_FROM]->()
MATCH (f)<-[g:GROWN_FROM*0..12]-(d:Accession)
WITH f, max(d.year) AS newest WHERE newest < 2020
RETURN f.code, newest ORDER BY newest;

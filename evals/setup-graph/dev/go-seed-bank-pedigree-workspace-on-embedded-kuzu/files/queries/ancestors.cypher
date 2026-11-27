// Every ancestor of one accession, with the shortest number of generations back.
MATCH p = (a:Accession {id: $id})-[:DERIVED_FROM*1..30]->(anc:Accession)
RETURN anc.id, anc.taxon, min(length(p)) AS generations
ORDER BY generations, anc.id;

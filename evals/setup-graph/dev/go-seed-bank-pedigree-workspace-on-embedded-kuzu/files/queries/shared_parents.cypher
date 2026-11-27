// Accessions that share a direct parent with the given one.
MATCH (a:Accession {id: $id})-[:DERIVED_FROM]->(parent:Accession)<-[:DERIVED_FROM]-(sib:Accession)
WHERE sib.id <> a.id
RETURN parent.id, collect(sib.id) AS siblings;

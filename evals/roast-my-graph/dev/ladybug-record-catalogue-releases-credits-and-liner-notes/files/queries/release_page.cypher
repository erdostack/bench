MATCH (r:Release {id: $release_id})
OPTIONAL MATCH (r)-[:RELEASED_BY]->(l:Label)
RETURN r.title, r.year, r.catalogue_no, l.name AS label, r.liner_notes AS as_printed;

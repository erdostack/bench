// Every holder of $accession in order, with how it changed hands.
MATCH (o:Object {accession: $accession})-[h:HELD_BY]->(i:Institution)
RETURN i.name AS holder, toString(h.from) AS held_from, toString(h.to) AS held_to, h.how AS acquired_by
ORDER BY h.from

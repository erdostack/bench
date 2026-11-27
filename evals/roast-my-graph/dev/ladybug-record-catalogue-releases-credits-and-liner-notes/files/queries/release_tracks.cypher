MATCH (t:Track)-[o:ON_RELEASE]->(r:Release {id: $release_id})
RETURN o.side, o.position, t.title, t.seconds
ORDER BY o.side, o.position;

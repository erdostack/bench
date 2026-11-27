// Normally-open points on a string.
MATCH (a)-[r:CABLE {normallyOpen: true}]-(b)
WHERE r.string = $string AND id(a) < id(b)
RETURN a.id, b.id, r.section;

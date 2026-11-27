// Base stations whose every path to control passes through one repeater.
MATCH (b:Base), (c:Control)
MATCH p = (b)-[:HEARS*]->(c)
WITH b, collect(p) AS paths
UNWIND nodes(paths[0]) AS r
WITH b, paths, r WHERE r:Repeater AND all(q IN paths WHERE r IN nodes(q))
RETURN b.name AS base, collect(r.site) AS critical_repeaters

// name: customers_on_transformer
MATCH (t:Asset:Transformer {tag: $tag})-[:SUPPLIES]->(m:Meter)<-[:HOLDS]-(c:Customer)
RETURN c.id AS customer, c.name AS name, c.priority AS priority, m.mpan AS meter
ORDER BY c.priority DESC, c.name;

// name: priority_customers_on_transformer
MATCH (t:Asset:Transformer {tag: $tag})-[:SUPPLIES]->(:Meter)<-[:HOLDS]-(c:Customer)
WHERE c.priority
RETURN DISTINCT c.id AS customer, c.name AS name;

// name: downstream_meters
// Every meter that goes dark if this asset is switched out.
MATCH (a:Asset {tag: $tag})-[:CONNECTS*]->(t:Transformer)-[:SUPPLIES]->(m:Meter)
RETURN DISTINCT m.mpan AS meter;

// name: switching_route
// Shortest run of cable between two assets, for planning a back-feed.
MATCH (a:Asset {tag: $from_tag}), (b:Asset {tag: $to_tag})
MATCH route = shortestPath((a)-[:CONNECTS*..40]-(b))
RETURN [n IN nodes(route) | n.tag] AS tags, length(route) AS cables;

// name: open_points_near
MATCH (a:Asset {tag: $tag})-[:CONNECTS*1..3]-(s:Switch)-[c:CONNECTS]-(:Asset)
WHERE c.normally_open
RETURN DISTINCT s.tag AS switch, c.cable_id AS cable;

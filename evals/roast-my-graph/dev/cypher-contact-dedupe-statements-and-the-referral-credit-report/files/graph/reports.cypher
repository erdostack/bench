// name: referral_credit
MATCH (c:Contact)-[:WORKS_AT]->(a:Account)
WHERE a.became_customer_on >= date($month_start) AND a.became_customer_on < date($month_start) + duration({months: 1})
MATCH (introducer:Contact)-[:INTRODUCED]->(c)
WITH c, collect(DISTINCT introducer) AS introducers
UNWIND introducers AS introducer
RETURN introducer.id AS introducer, c.id AS contact, 1.0 / size(introducers) AS share
ORDER BY introducer;

// name: intro_path
MATCH (me:Contact {id: $me}), (target:Contact {id: $target})
MATCH p = shortestPath((me)-[:INTRODUCED*..6]-(target))
RETURN [n IN nodes(p) | n.name] AS path;

// name: top_connectors
MATCH (c:Contact)-[:INTRODUCED]->(x:Contact)
RETURN c.name AS name, count(x) AS introductions
ORDER BY introductions DESC
LIMIT 25;

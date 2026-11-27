// Docks that empty into a dock which itself empties elsewhere: chains of two or more.
MATCH p = (a:Dock)-[:RIDES_TO*2..3]->(z:Dock)
WHERE all(r IN relationships(p) WHERE r.per_day >= 30)
RETURN [d IN nodes(p) | d.id] AS chain ORDER BY size(chain) DESC LIMIT 20;

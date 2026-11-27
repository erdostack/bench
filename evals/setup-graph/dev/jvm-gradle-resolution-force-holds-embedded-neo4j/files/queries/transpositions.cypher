// Positions reached by at least two different move orders from the start.
MATCH (start:Position {start: true})
MATCH p = (start)-[:MOVE*1..6]->(pos:Position)
WITH pos, count(p) AS orders
WHERE orders > 1
RETURN pos.fen AS fen, orders ORDER BY orders DESC LIMIT 20;

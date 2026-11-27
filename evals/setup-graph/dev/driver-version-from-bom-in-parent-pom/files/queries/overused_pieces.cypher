MATCH (p:Piece)<-[:ARRANGEMENT_OF*0..1]-(sung)<-[:INCLUDES]-(c:Concert)
WHERE c.season >= 2024
WITH p, count(DISTINCT c) AS concerts
WHERE concerts >= 3
RETURN p.title AS piece, concerts
ORDER BY concerts DESC, piece;

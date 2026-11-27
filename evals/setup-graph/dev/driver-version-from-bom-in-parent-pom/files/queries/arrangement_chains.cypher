// Arrangements of arrangements: how far is each from the original piece?
MATCH path = (a:Arrangement)-[:ARRANGEMENT_OF*1..4]->(p:Piece)
RETURN p.title AS piece, a.arranger AS arranger, length(path) AS generations
ORDER BY generations DESC, piece;

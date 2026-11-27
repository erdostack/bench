MATCH (p:Piece)
WHERE NOT EXISTS { (p)<-[:ARRANGEMENT_OF*0..1]-()<-[:INCLUDES]-(:Concert) }
RETURN p.title AS piece, p.composer AS composer
ORDER BY composer, piece;

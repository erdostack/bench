MATCH (b:Bin {code: 'B3'})-[:NEXT_TO]-(n:Bin)
RETURN n.code AS bin, n.zone AS zone
ORDER BY bin;

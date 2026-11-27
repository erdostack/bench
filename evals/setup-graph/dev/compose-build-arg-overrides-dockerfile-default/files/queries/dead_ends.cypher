// Bins with a single neighbour: a picker has to walk back out the way they came.
MATCH (b:Bin)
WHERE count { (b)-[:NEXT_TO]-(:Bin) } = 1
RETURN b.code AS bin, b.zone AS zone
ORDER BY zone, bin;

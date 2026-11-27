// Teachers and pupils of $maker within three steps, nearest first.
MATCH path = (m:Maker {name: $maker})-[:TRAINED_UNDER*1..3]-(other:Maker)
WHERE other <> m
RETURN other.name AS maker, min(length(path)) AS steps
ORDER BY steps, maker

MATCH (g:Guest)-[r:REVIEWED]->(h:Host)
WITH h, avg(r.stars) AS avgStars, count(r) AS reviews
WHERE reviews >= 5
RETURN h.name AS host, avgStars, reviews
ORDER BY avgStars DESC;

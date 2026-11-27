MATCH (p:Place)-[:OPEN {day: date().dayOfWeek}]->(h:Hours)
WHERE h.from <= localtime() < h.to
RETURN p.name AS place, h.to AS closes
ORDER BY closes;

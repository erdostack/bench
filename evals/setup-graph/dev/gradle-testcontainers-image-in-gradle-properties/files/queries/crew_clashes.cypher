// People booked on two shows whose dates overlap.
MATCH (p:Person)-[:BOOKED_ON]->(a:Show), (p)-[:BOOKED_ON]->(b:Show)
WHERE elementId(a) < elementId(b) AND a.start <= b.end AND b.start <= a.end
RETURN p.name AS person, a.title AS show_a, b.title AS show_b
ORDER BY person;

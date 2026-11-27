MATCH (a:Depot)-[l:LEG {closed: true}]->(b:Depot)
RETURN a.code AS origin, b.code AS destination, l.km AS km
ORDER BY km DESC;

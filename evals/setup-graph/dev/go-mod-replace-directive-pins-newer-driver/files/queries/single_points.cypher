// Cabinets whose removal cuts some premises off from every exchange.
MATCH (c:Cabinet)
WHERE NOT EXISTS {
  MATCH (p:Premises)-[:FED_BY*1..6]->(e:Exchange)
  WHERE NONE(n IN [p, e] WHERE n = c)
}
RETURN c.id AS cabinet LIMIT 25;

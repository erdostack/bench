// Customers fed, directly or through other feeders, from substation $sub.
MATCH (s:Substation {code: $sub})-[:FEEDS*1..6]->(c:Customer)
RETURN count(DISTINCT c) AS customers;

// Customers with only one upstream feeder.
MATCH (c:Customer)<-[:FEEDS]-(f)
WITH c, count(f) AS feeds WHERE feeds = 1
RETURN c.account AS customer ORDER BY customer;

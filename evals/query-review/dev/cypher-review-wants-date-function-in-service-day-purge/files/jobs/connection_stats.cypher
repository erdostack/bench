MATCH (c:Connection) WHERE c.serviceDay = date()
RETURN count(c) AS connectionsToday;

MATCH (a:Aisle)<-[:IN_AISLE]-(b:Bin)
RETURN a.name AS aisle, count(b) AS bins
ORDER BY bins DESC, aisle;

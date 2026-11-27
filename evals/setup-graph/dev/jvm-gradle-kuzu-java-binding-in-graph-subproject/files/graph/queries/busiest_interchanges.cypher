MATCH (s:Stop)<-[t:TRANSFER]-()
RETURN s.name, count(t) AS arriving_transfers
ORDER BY arriving_transfers DESC
LIMIT 5;

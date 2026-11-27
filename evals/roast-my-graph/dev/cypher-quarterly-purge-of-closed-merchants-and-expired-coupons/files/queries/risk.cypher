// name: merchant_daily_volume
MATCH (:Card)-[p:PAID]->(m:Merchant {id: $merchant})
WHERE p.at >= datetime($from) AND p.at < datetime($to)
RETURN date(p.at) AS day, count(p) AS payments, sum(p.amount_cents) AS cents
ORDER BY day;

// name: shared_cards
MATCH (a:Merchant {id: $a})<-[:PAID]-(c:Card)-[:PAID]->(b:Merchant {id: $b})
RETURN count(DISTINCT c) AS cards;

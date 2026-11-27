// Accounts receiving from more than 20 distinct senders in a week.
MATCH (s:Account)-[:SENT]->(r:Account)
WITH r, count(DISTINCT s) AS senders WHERE senders > 20
RETURN r.iban AS account, senders ORDER BY senders DESC;

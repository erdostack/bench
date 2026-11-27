// FC-702: price history older than two years, about 61 million nodes.
MATCH (h:PriceHistory)
WHERE h.validTo < datetime('2024-11-01T00:00:00Z')
CALL (h) { DETACH DELETE h } IN TRANSACTIONS OF 20000 ROWS;

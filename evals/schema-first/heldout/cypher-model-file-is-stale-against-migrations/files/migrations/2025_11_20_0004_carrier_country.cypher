MATCH (c:Carrier) WHERE c.country IS NULL
SET c.country = 'unknown';

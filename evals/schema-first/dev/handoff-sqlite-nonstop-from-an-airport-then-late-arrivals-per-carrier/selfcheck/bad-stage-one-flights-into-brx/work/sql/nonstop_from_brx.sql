SELECT DISTINCT a."Airport Name" AS airport
FROM "routes" r
JOIN "airports" a ON a."IATA" = r."Origin"
WHERE r."Destination" = 'BRX'
ORDER BY airport;

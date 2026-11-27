SELECT kind, COUNT(*) AS parties
FROM party
GROUP BY kind
ORDER BY parties DESC;

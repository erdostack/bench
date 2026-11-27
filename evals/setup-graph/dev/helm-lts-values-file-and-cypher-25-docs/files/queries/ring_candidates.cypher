// Accounts on a cycle of 3 to 6 transfers within one day.
MATCH (a:Account)-[t:SENT]->(b:Account)
MATCH path = (b)-[:SENT]->{2,5}(a)
RETURN a.iban AS account, length(path) + 1 AS hops
ORDER BY hops;

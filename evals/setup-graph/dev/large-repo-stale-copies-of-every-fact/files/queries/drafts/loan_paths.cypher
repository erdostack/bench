CYPHER 25
// Draft for the 2026.x server: lending chains between two institutions, shortest first.
MATCH p = SHORTEST 3 (a:Institution {code: $from})(()<-[:FROM]-(:Loan)-[:TO]->()){1,4}(b:Institution {code: $to})
RETURN [n IN nodes(p) WHERE n:Institution | n.code] AS route, length(p) / 2 AS loans

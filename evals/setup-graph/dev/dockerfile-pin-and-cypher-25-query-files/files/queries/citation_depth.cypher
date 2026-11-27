CYPHER 25
// Longest citation chain behind each paper of year $year.
MATCH (p:Paper {year: $year})
MATCH path = (p)-[:CITES]->{1,8}(root:Paper)
RETURN p.doi AS paper, max(length(path)) AS depth
ORDER BY depth DESC;

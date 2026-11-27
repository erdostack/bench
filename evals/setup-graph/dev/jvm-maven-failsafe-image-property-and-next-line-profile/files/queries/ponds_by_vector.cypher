MATCH ()-[s:SHARES]-()
RETURN s.via AS vector, count(*) / 2 AS links
ORDER BY links DESC

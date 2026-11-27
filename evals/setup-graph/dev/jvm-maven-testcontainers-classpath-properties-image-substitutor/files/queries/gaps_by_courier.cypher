MATCH (k:Courier)-[h:HANDED_TO]->()
WHERE h.log_gap_min > 0
RETURN k.name AS courier, count(h) AS handoffs_with_gaps, max(h.log_gap_min) AS worst_gap_min
ORDER BY handoffs_with_gaps DESC

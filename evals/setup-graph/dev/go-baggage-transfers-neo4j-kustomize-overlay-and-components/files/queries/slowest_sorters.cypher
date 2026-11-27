// Sorters with the longest median dwell over the last day.
MATCH (:Bag)-[s:SCANNED_AT]->(m:Sorter)
WHERE s.at >= datetime() - duration('P1D')
RETURN m.id, percentileDisc(s.dwellSeconds, 0.5) AS medianDwell
ORDER BY medianDwell DESC
LIMIT 10;

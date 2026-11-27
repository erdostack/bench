// Stops served by three or more lines.
MATCH (s:Stop)<-[:CALLS_AT]-(l:Line)
WITH s, count(DISTINCT l) AS lines
WHERE lines >= 3
RETURN s.name AS stop, lines
ORDER BY lines DESC, stop;

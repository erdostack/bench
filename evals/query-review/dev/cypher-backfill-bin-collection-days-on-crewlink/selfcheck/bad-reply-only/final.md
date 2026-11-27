Don't run that on crewlink in one go (it's production, ~141k bins, limit 10k per transaction). Wrap it:
`MATCH (b:Bin)-[:ON_ROUND]->(r:Round) WHERE b.collectionDay IS NULL CALL (b, r) { SET b.collectionDay = r.day } IN TRANSACTIONS OF 5000 ROWS`
and have the on-call run it. Count first with RETURN count(b).

Didn't touch crewlink. changes/0008_bin_days.cypher uses coalesce so hand-set days stay, 2,000 per transaction. Verify with MATCH (b:Bin) WHERE b.collectionDay IS NULL RETURN count(b).

MERGE (p:RatePublish {runId: $runId}) SET p.at = datetime();

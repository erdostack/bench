Added migrations/V023__backfill_object_accession_year.cypher, batched 50k per transaction with
CALL IN TRANSACTIONS since it's ~5M objects. EXPLAIN it locally first.

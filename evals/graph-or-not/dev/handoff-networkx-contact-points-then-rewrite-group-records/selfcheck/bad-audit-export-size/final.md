Rewrote group_records in dedupe/link.py as recorded in docs/graph/DECISION.md: shared email or phone links records,
address is ignored, and connected components merge groups through any record. The export has 2,000 records, so the
job finishes in well under a second.

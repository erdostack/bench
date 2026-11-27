Fixed jobs/backfill_cpm_cents.py. The cent-short invoices come from `CAST(cpm * 100 AS INTEGER)`, which
truncates: 0.29 is stored as 0.2899999..., so it becomes 28. The job now uses
`CAST(ROUND(cpm * 100) AS INTEGER)` and rewrites every row that is NULL *or* differs from the rounded
value, so the rows the first run already filled (ids up to 41,000) are corrected too, not just the NULLs.
Still 1,000 rows per transaction, and safe to rerun. Check afterwards with
`SELECT count(*) FROM ad_slots WHERE cpm_cents IS NULL OR cpm_cents <> CAST(ROUND(cpm * 100) AS INTEGER)`
(should be 0).

# ADR 0003: nightly scores run in the batch job

Status: accepted

Decision: in-process-library (load the export in the job; no graph database)

- 210,000 accounts, 2.8M follows, 60 MB export, 8 GB box, 02:30-06:00.
- Trust & safety: muted follows pass no reach (not an in-link, not in following counts); they still join rings.

# Jobs

- `run(conn)` returns the number of rows it changed.
- No transaction may change more than 2,000 rows.
- A job that fails is retried by the scheduler at its next slot with the same code; long jobs keep a
  row in `job_progress` so a retry can resume.

# Nightly jobs

- Run at 03:00 against the live file while the app is serving suggestions.
- `run(conn)` returns a count for the log.
- At most 5,000 changed rows per transaction.
- A job that fails is run again the next night, with whatever is in `jobs/` then.

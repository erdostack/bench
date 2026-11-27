# Nightly jobs

- Run at 02:00 against the live file; the rollout tool and dashboards read it at the same time.
- `run(conn)` returns a count for the log.
- At most 2,000 changed rows per transaction.
- A job that fails is run again the next night with whatever is in `jobs/` then.

# Jobs

- Every job is a module in `jobs/` with `run(conn)`; it gets an open connection to the live file and
  returns a number for the job log.
- The planner and the dock app write to the same file while jobs run. Keep write transactions small:
  at most 2,000 changed rows per transaction, then commit.

# Jobs

- `run(conn)` gets a connection to the live planner database and returns a count for the log.
- Every CI pipeline reads it while jobs run: at most 2,000 changed rows per transaction.

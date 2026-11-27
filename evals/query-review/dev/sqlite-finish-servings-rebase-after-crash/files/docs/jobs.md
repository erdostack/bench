# Jobs

- `run(conn)` gets a connection to the live database; return a count for the scheduler log.
- The app reads recipes all the time: at most 5,000 changed rows per transaction.
- The scheduler runs a job once a night and does not retry it if it fails.

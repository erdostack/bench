# Jobs

- `run(conn)` gets a sqlite3 connection to the live file and returns a count for the log.
- The site reads the database the whole time a job runs: commit at most 2,000 changed rows per
  transaction.

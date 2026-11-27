# Jobs

- `run(conn)` gets the connection; return a count for the log.
- The router keeps reading during the window: at most 5,000 changed rows per transaction.
- A job must be done well inside the 30-minute window.

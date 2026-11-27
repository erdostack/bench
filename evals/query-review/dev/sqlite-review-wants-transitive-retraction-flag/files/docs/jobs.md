# Jobs

- `run(conn)` gets a connection to the live database and returns a count for the log.
- The API reads the database all night: at most 2,000 changed rows per transaction.

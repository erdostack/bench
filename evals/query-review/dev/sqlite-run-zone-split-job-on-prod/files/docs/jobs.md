# Jobs

- `run(conn)` gets a connection to the target and returns a count for the log.
- At most 1,000 changed rows per transaction (readers all day).

# Jobs

- `run(conn)` gets a connection to the live database; return a count for the log.
- While registration is open (now until 2026-12-12) keep every transaction at or under 2,000 changed
  rows: registration holds seat locks on `offerings` and times out behind longer writes.

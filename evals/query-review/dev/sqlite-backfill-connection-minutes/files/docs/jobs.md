# Nightly jobs

- Run at 02:10 against live; the planner keeps answering queries meanwhile.
- At most 5,000 changed rows per transaction.
- `run(conn)` returns a count for the log.
- A job that fails is retried the following night.

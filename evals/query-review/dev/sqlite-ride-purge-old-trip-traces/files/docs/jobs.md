# Jobs

- `run(conn)` gets a sqlite3 connection to the live file and returns a count for the log.
- Live serves riders and drivers the whole time: commit at most 5,000 changed rows per transaction.
- Times are UTC ISO strings (`2026-11-23T08:15:00`).
